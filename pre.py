import argparse
import logging
import os
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from osgeo import gdal

gdal.UseExceptions()

from DANet.DANet import DANet
from utils.data_loading import BasicDataset

# 读取影像函数
def read_img(filename):
    ds = gdal.Open(filename)
    if ds is None:
        raise FileNotFoundError(f"无法打开文件: {filename}")
    width, height = ds.RasterXSize, ds.RasterYSize
    data = ds.ReadAsArray(0, 0, width, height)
    ds = None
    return data

# 二分类IoU等指标
class IOUMetric:
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.hist = np.zeros((num_classes, num_classes))

    def _fast_hist(self, lp, lt):
        mask = (lt >= 0) & (lt < self.num_classes)
        hist = np.bincount(
            self.num_classes * lt[mask].astype(int) + lp[mask],
            minlength=self.num_classes ** 2
        ).reshape(self.num_classes, self.num_classes)
        return hist

    def evaluate(self, preds, gts):
        for p, t in zip(preds, gts):
            self.hist += self._fast_hist(p.flatten(), t.flatten())
        tp = np.diag(self.hist)
        union = self.hist.sum(axis=1) + self.hist.sum(axis=0) - tp
        iou = tp / union
        miou = np.nanmean(iou)
        dice = 2 * tp / (self.hist.sum(axis=1) + self.hist.sum(axis=0))
        f1 = np.nanmean(dice)
        acc = tp.sum() / self.hist.sum()
        return acc, miou, f1

# 读取并归一化tif
def read_and_convert_tif(fp):
    ds = gdal.Open(fp)
    if ds is None:
        return None
    arr = ds.GetRasterBand(1).ReadAsArray()
    ds = None
    if arr.dtype == np.float64:
        arr = (arr * 255).astype(np.uint8)
    return arr.astype(np.uint8)

# 单张预测函数
def predict_img(net, img, device, scale=1, thr=0.5):
    net.eval()
    x = torch.from_numpy(BasicDataset.preprocess(img, scale, is_mask=False)).unsqueeze(0)
    x = x.to(device=device, dtype=torch.float32)
    with torch.no_grad():
        out = net(x)
        if net.n_classes > 1:
            prob = F.softmax(out, dim=1)[0]
        else:
            prob = torch.sigmoid(out)[0]
        tf = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor()
        ])
        mask = tf(prob.cpu()).squeeze()
    if net.n_classes == 1:
        return (mask > thr).numpy().astype(np.uint8)
    else:
        return F.one_hot(mask.argmax(dim=0), net.n_classes).permute(2, 0, 1).numpy().astype(np.uint8)

# Mask转图像
def mask_to_image(mask):
    if mask.ndim == 2:
        return Image.fromarray((mask * 255).astype(np.uint8))
    else:
        return Image.fromarray((np.argmax(mask, axis=0) * 255).astype(np.uint8))

# 可视化App
class VisualizationApp:
    def __init__(self, root, net, device):
        self.root = root
        self.net = net
        self.device = device
        root.title("图像分割可视化工具")

        # 左侧显示区
        lf = tk.Frame(root)
        lf.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas_orig = tk.Canvas(lf, width=512, height=512)
        self.canvas_orig.pack()
        self.canvas_pred = tk.Canvas(lf, width=512, height=512)
        self.canvas_pred.pack()

        # 右侧控制区
        rf = tk.Frame(root)
        rf.pack(side=tk.RIGHT, padx=10, pady=10)
        self.btn_select = tk.Button(rf, text="选择目录", command=self.select_dir)
        self.btn_select.pack(pady=5)
        self.btn_run = tk.Button(rf, text="运行并显示", command=self.run_pipeline)
        self.btn_run.pack(pady=5)
        self.txt = tk.Text(rf, width=40, height=15)
        self.txt.pack(pady=5)

        self.test_dir = self.label_dir = self.out_dir = None

    def select_dir(self):
        self.test_dir = filedialog.askdirectory(title="选择测试图像目录")
        self.label_dir = filedialog.askdirectory(title="选择标签目录")
        self.out_dir = filedialog.askdirectory(title="选择输出目录")
        self.txt.insert(tk.END, f"已选：\n测试：{self.test_dir}\n标签：{self.label_dir}\n输出：{self.out_dir}\n")

    def run_pipeline(self):
        if not all([self.test_dir, self.label_dir, self.out_dir]):
            self.txt.insert(tk.END, "请先选择所有目录！\n")
            return
        files = [f for f in os.listdir(self.test_dir) if f.lower().endswith(('.tif','.png','.jpg'))]
        preds, gts = [], []
        # 预测并保存
        for name in files:
            img = read_img(os.path.join(self.test_dir, name))
            mask = predict_img(self.net, img, self.device)
            preds.append(mask)
            mask_to_image(mask).save(os.path.join(self.out_dir, name))
        # 读取真值
        for name in files:
            gt = read_and_convert_tif(os.path.join(self.label_dir, name))
            if gt is not None:
                gts.append(gt)
        acc, miou, f1 = IOUMetric(2).evaluate(preds, gts)
        self.txt.insert(tk.END, f"准确率: {acc:.4f}\nmIoU: {miou:.4f}\nF1: {f1:.4f}\n")
        # 显示最后一张
        self.display(img, mask)

    def display(self, orig, mask):
        # 原图
        if orig.ndim == 3:
            orig = orig[0]
        pil_o = Image.fromarray(orig.astype(np.uint8)).resize((512, 512))
        tk_o = ImageTk.PhotoImage(pil_o)
        self.canvas_orig.create_image(0, 0, anchor=tk.NW, image=tk_o)
        self.canvas_orig.image = tk_o
        # 预测结果
        pil_m = mask_to_image(mask).resize((512, 512))
        tk_m = ImageTk.PhotoImage(pil_m)
        self.canvas_pred.create_image(0, 0, anchor=tk.NW, image=tk_m)
        self.canvas_pred.image = tk_m

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = DANet(nclass=2, backbone='resnet50', pretrained_base=False, aux=False)
    net.load_state_dict(torch.load('./Bishejzw_checkpoints_DANet/checkpoint_epoch50.pth', map_location=device))
    root = tk.Tk()
    app = VisualizationApp(root, net, device)
    root.mainloop()
