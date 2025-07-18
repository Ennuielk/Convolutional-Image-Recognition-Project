import os
import random
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.image import imread
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import load_model
import streamlit as st
# 加载模型和数据集（这部分代码应该已经在您的应用中）
model_path = r"C:\Users\yxh\Desktop\transfer_model2.h5"
model = load_model(model_path)

# 创建数据集（示例代码，您需要根据实际情况调整）
train_path = r"C:\Users\yxh\Desktop\Fruit_dataset\train1"
test_path = r"C:\Users\yxh\Desktop\Fruit_dataset\val1"
BATCH_SIZE = 32
IMG_SIZE = (224, 224)

test_dataset = image_dataset_from_directory(
    test_path,
    shuffle=False,
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    label_mode='categorical',
    seed=42
)
class_names = test_dataset.class_names


# 修改后的plot_predictions函数，返回图形对象而不是直接显示
def st_plot_predictions(model, dataset, class_names, num_images=10):
    # 收集图像和标签
    all_images = []
    all_labels = []

    for images, labels in dataset.unbatch():
        all_images.append(images)
        all_labels.append(labels)

    all_images = np.array(all_images)
    all_labels = np.array(all_labels)

    # 随机选择图像
    random_indices = random.sample(range(len(all_images)), min(num_images, len(all_images)))
    selected_images = all_images[random_indices]
    selected_labels = all_labels[random_indices]

    # 预测
    predictions = model.predict(selected_images)
    predicted_labels = tf.argmax(predictions, axis=1)
    true_labels = tf.argmax(selected_labels, axis=1)

    # 创建图形
    fig, axes = plt.subplots(2, 5, figsize=(20, 12))
    axes = axes.ravel()

    for i in range(len(random_indices)):
        axes[i].imshow(selected_images[i].astype("uint8"))

        # 获取预测信息
        pred_class = class_names[predicted_labels[i]]
        true_class = class_names[true_labels[i]]
        confidence = np.max(predictions[i]) * 100

        # 设置标题颜色
        color = 'green' if predicted_labels[i] == true_labels[i] else 'red'

        # 设置标题
        axes[i].set_title(f"Pred: {pred_class}\nTrue: {true_class}\nConf: {confidence:.1f}%",
                          color=color, fontsize=10)
        axes[i].axis('off')

    fig.suptitle(f"Fine-Tuned ENB0 Predictions on Validation Set\n(Green=Correct, Red=Incorrect)",
                 fontsize=14, y=1.02)
    plt.tight_layout()

    # 计算准确率
    accuracy = np.mean(predicted_labels == true_labels)

    # 返回图形和准确率
    return fig, accuracy


# Streamlit界面
st.title("水果分类模型评估")

if st.button("运行模型评估"):
    with st.spinner('正在评估模型...'):
        fig, accuracy = st_plot_predictions(model, test_dataset, class_names)

        # 显示结果
        st.pyplot(fig)
        st.success(f"样本准确率: {accuracy:.2%}")

        # 显示混淆矩阵（如果类别不多）
        if len(class_names) <= 20:
            st.subheader("混淆矩阵")

            # 需要重新计算所有预测以生成完整的混淆矩阵
            all_preds = []
            all_true = []
            for images, labels in test_dataset.unbatch():
                pred = model.predict(np.expand_dims(images, axis=0))
                all_preds.append(np.argmax(pred))
                all_true.append(np.argmax(labels))

            cm = confusion_matrix(all_true, all_preds)
            st.write(cm)