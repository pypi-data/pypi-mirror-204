# encoding: utf-8
# @author: k

import datetime
import argparse
import logging
from tqdm import tqdm
import os
import time

import numpy as np
import torch
from transformers import BertTokenizer, BertConfig, BertModel
from torch.utils import data
from sklearn.model_selection import train_test_split

from ..utils.init_args import setup_classification_args
from ..utils.init_logger import setup_logger

args = setup_classification_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

if not os.path.exists(args.train_path):
    raise Exception(f"file:{args.train_path} does not exist.")

print("开始读取数据")
with open(args.train_path, "r", encoding=args.encoding) as f:
    datas = f.readlines()

datas = [x.strip() for x in datas]
print("读取数据完成")

info_labels = []

# 加载预训练模型
pretrained = args.pretrained_model
tokenizer = BertTokenizer.from_pretrained(pretrained)
bert_model = BertModel.from_pretrained(pretrained)
config = BertConfig.from_pretrained(pretrained)


def get_label(x):
    if isinstance(x, str):
        if x not in info_labels:
            info_labels.append(x)
        return info_labels.index(x)
    else:
        return info_labels[x]


def get_train_test_data(max_length=args.max_length, test_size=args.test_size):
    texts = []
    labels = []

    for one in tqdm(datas):
        result = one.split(args.split_data)
        if len(result) != 2:
            continue

        text, label = result
        try:
            lebal_index = get_label(label.strip())
            text = tokenizer.encode(text.strip(), max_length=max_length, padding="max_length",
                                    truncation="longest_first")
            texts.append(text)
            labels.append(lebal_index)
        except Exception as e:
            print(e)
            continue
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=test_size, random_state=0,
                                                        shuffle=True)
    return (X_train, y_train), (X_test, y_test)


print("开始转换数据")
(X_train, y_train), (X_test, y_test) = get_train_test_data(test_size=0.1)
print("完成转换数据")

label_path = os.path.join(args.save_dir, args.label_file_name)

with open(label_path, "w", encoding=args.encoding) as f:
    for label in info_labels:
        f.write(f"{label}\n")
print(f"保存标签至:[{label_path}]")


# dataloader
class DataGen(data.Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return np.array(self.data[index]), np.array(self.label[index])


batch_size = args.batch_size
train_dataset = DataGen(X_train, y_train)
test_dataset = DataGen(X_test, y_test)
train_dataloader = data.DataLoader(train_dataset, batch_size=batch_size)
test_dataloader = data.DataLoader(test_dataset, batch_size=batch_size)


class Model(torch.nn.Module):
    def __init__(self, bert_model, bert_config, num_class):
        super(Model, self).__init__()
        self.bert_model = bert_model
        self.dropout = torch.nn.Dropout(0.4)
        self.fc1 = torch.nn.Linear(bert_config.hidden_size, bert_config.hidden_size)
        self.fc2 = torch.nn.Linear(bert_config.hidden_size, num_class)
        self.relu = torch.nn.ReLU()

    def forward(self, token_ids):
        bert_out = self.bert_model(token_ids)[1]  # 句向量 [batch_size,hidden_size]
        bert_out = self.dropout(bert_out)
        bert_out = self.fc1(bert_out)
        bert_out = self.relu(bert_out)
        bert_out = self.dropout(bert_out)
        bert_out = self.fc2(bert_out)  #
        return bert_out


model = Model(bert_model, config, len(info_labels))
if args.device and args.device.startswith("cuda"):
    device = torch.device(args.device) if torch.cuda.is_available() else 'cpu'
elif args.device == "cpu":
    device = torch.device("cpu")
else:
    device = torch.device(args.device)
print(f"训练使用device:[{device}]")
model.to(device)


def get_optimizer():
    select_optimizer = args.optimizer
    if select_optimizer == "sgd":
        optimizer = torch.optim.SGD(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    return optimizer


criterion = torch.nn.CrossEntropyLoss()
optimizer = get_optimizer()


def start_train():
    print("开始训练数据")
    best_accu = 0
    for epoch in range(args.num_epochs):
        print(f"epoch = {epoch}, datetime = {datetime.datetime.now()}")
        start = time.time()
        loss_sum = 0.0
        accu = 0
        model.train()
        for token_ids, label in tqdm(train_dataloader):
            token_ids = token_ids.to(device).long()
            label = label.to(device).long()
            out = model(token_ids)
            loss = criterion(out, label)
            optimizer.zero_grad()
            loss.backward()  # 反向传播
            optimizer.step()  # 梯度更新
            loss_sum += loss.cpu().data.numpy()
            accu += (out.argmax(1) == label).sum().cpu().data.numpy()

        test_loss_sum = 0.0
        test_accu = 0
        model.eval()
        for token_ids, label in tqdm(test_dataloader):
            token_ids = token_ids.to(device).long()
            label = label.to(device).long()
            with torch.no_grad():
                out = model(token_ids)
                loss = criterion(out, label)
                test_loss_sum += loss.cpu().data.numpy()
                test_accu += (out.argmax(1) == label).sum().cpu().data.numpy()
        accuracy = test_accu / len(test_dataset)
        print("epoch %d, train loss:%f, train acc:%f, test loss:%f, test acc:%f, use time:" % (
            epoch, loss_sum / len(train_dataset), accu / len(train_dataset), test_loss_sum / len(test_dataset),
            test_accu / len(test_dataset)), int(time.time() - start))
        if args.save_best:
            # 如果只保存最优模型
            if best_accu < accuracy:
                save_path = os.path.join(args.save_dir, f"{args.job_type}_model_best.pt")
                best_accu = accuracy
                torch.save(model.state_dict(), save_path)
        else:
            save_path = os.path.join(args.save_dir, f"{args.job_type}_model_{epoch}_{test_accu / len(test_dataset)}.pt")
            torch.save(model.state_dict(), save_path)
