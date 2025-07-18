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
from PIL import Image
import sqlite3
# 加载模型和数据集（这部分代码应该已经在您的应用中）
model_path = r"C:\Users\Ennuielk\Documents\transfer_model2.h5"
model = load_model(model_path)

# 创建数据集（示例代码，您需要根据实际情况调整）
train_path = r"C:\Users\Ennuielk\Documents\archive\Fruit_dataset\train1"
test_path = r"C:\Users\Ennuielk\Documents\archive\Fruit_dataset\val1"
BATCH_SIZE = 32
IMG_SIZE = (224, 224)

#数据库


def get_fruit_nutrition(fruit_name):
    """获取特定水果的营养信息"""
    conn = sqlite3.connect('fruit.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM fruits WHERE name = ?', (fruit_name,))
    result = cursor.fetchone()
    conn.close()

    return dict(result)


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


def predict_fruit():
    fruits = [f"水果_{i}" for i in range(1, 101)]  # 生成100种水果名称
    return np.random.choice(fruits), np.random.rand()


def preprocess_image(img_raw):
    #转换为tensor
    img = np.array(img_raw, dtype=np.float32)
    # 调整尺寸为 (224, 224)
    img = tf.image.resize(img, [224, 224])
    img = tf.expand_dims(img, axis=0)
    return img
def predict_function(img):
    predictions = model.predict(img)
    predicted_labels = tf.argmax(predictions, axis=1)
    pred_class = class_names[predicted_labels[0]]
    fruit_info = get_fruit_nutrition(pred_class)
    return pred_class,fruit_info


# Streamlit界面
# 创建侧边栏导航
st.sidebar.title("导航")
page = st.sidebar.radio("选择页面", ["模型评估", "应用"])

if page == "模型评估":
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

elif page == "应用":
    st.title("应用")
    st.write("这里是查询水果名称及营养价值的页面")
    # 在这里添加其他功能的代码
    uploaded = st.file_uploader("上传水果图片", type=["jpg", "png"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, width=200)
        img = preprocess_image(img)
        pred_class,fruit_info = predict_function(img)
        if st.button("查询水果名称及营养价值"):
            st.write(pred_class,fruit_info)
            #st.success(f"预测结果: {fruit} (置信度: {prob:.2f})")
            st.balloons()
