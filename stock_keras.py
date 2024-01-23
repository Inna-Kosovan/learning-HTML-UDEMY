# {
#  "cells": [],
#  "metadata": {
#   "language_info": {
#    "name": "python"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 2
# }

# {
#  "cells": [
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "# uncomment below line of code if you want to calculate features and save dataframe\n",
#     "# this script prints the path at which dataframe with calculated features is saved.\n",
#     "# train.py calls the DataGenerator class to \n",
#     "\n",
#     "# %run ./train.py WMT original\n",
#     "\n",
#     "# this notebook was trained on cloud compute. So use your own paths"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "_cell_guid": "",
#     "_uuid": "",
#     "scrolled": true
#    },
#    "outputs": [],
#    "source": [
#     "import pandas as pd\n",
#     "import pickle \n",
#     "import numpy as np\n",
#     "from tqdm import tqdm_notebook as tqdm\n",
#     "from IPython.core.interactiveshell import InteractiveShell\n",
#     "\n",
#     "\n",
#     "np.random.seed(2)\n",
#     "company_code = 'WMT'\n",
#     "strategy_type = 'original'\n",
#     "# use the path printed in above output cell after running stock_cnn.py. It's in below format\n",
#     "df = pd.read_csv(\"../outputs/fresh_rolling_train/df_\"+company_code+\".csv\")\n",
#     "df['labels'] = df['labels'].astype(np.int8)\n",
#     "if 'dividend_amount' in df.columns:\n",
#     "    df.drop(columns=['dividend_amount', 'split_coefficient'], inplace=True)\n",
#     "display(df.head())"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "Split data into Training, Validation and Test"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "from sklearn.preprocessing import MinMaxScaler, OneHotEncoder\n",
#     "from sklearn.model_selection import train_test_split\n",
#     "# from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler\n",
#     "from collections import Counter\n",
#     "\n",
#     "list_features = list(df.loc[:, 'open':'eom_26'].columns)\n",
#     "print('Total number of features', len(list_features))\n",
#     "x_train, x_test, y_train, y_test = train_test_split(df.loc[:, 'open':'eom_26'].values, df['labels'].values, train_size=0.8, \n",
#     "                                                    test_size=0.2, random_state=2, shuffle=True, stratify=df['labels'].values)\n",
#     "\n",
#     "# smote = RandomOverSampler(random_state=42, sampling_strategy='not majority')\n",
#     "# x_train, y_train = smote.fit_resample(x_train, y_train)\n",
#     "# print('Resampled dataset shape %s' % Counter(y_train))\n",
#     "\n",
#     "if 0.7*x_train.shape[0] < 2500:\n",
#     "    train_split = 0.8\n",
#     "else:\n",
#     "    train_split = 0.7\n",
#     "# train_split = 0.7\n",
#     "print('train_split =',train_split)\n",
#     "x_train, x_cv, y_train, y_cv = train_test_split(x_train, y_train, train_size=train_split, test_size=1-train_split, \n",
#     "                                                random_state=2, shuffle=True, stratify=y_train)\n",
#     "mm_scaler = MinMaxScaler(feature_range=(0, 1)) # or StandardScaler?\n",
#     "x_train = mm_scaler.fit_transform(x_train)\n",
#     "x_cv = mm_scaler.transform(x_cv)\n",
#     "x_test = mm_scaler.transform(x_test)\n",
#     "\n",
#     "x_main = x_train.copy()\n",
#     "print(\"Shape of x, y train/cv/test {} {} {} {} {} {}\".format(x_train.shape, y_train.shape, x_cv.shape, y_cv.shape, x_test.shape, y_test.shape))"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "Out of total 441+ features select top 'N' features (let's include base features like close, adjusted_close etc)"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "num_features = 225  # should be a perfect square\n",
#     "selection_method = 'all'\n",
#     "topk = 320 if selection_method == 'all' else num_features\n",
#     "# if train_split >= 0.8:\n",
#     "#     topk = 400\n",
#     "# else:\n",
#     "#     topk = 300"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "%%time\n",
#     "from operator import itemgetter\n",
#     "from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif\n",
#     "\n",
#     "if selection_method == 'anova' or selection_method == 'all':\n",
#     "    select_k_best = SelectKBest(f_classif, k=topk)\n",
#     "    if selection_method != 'all':\n",
#     "        x_train = select_k_best.fit_transform(x_main, y_train)\n",
#     "        x_cv = select_k_best.transform(x_cv)\n",
#     "        x_test = select_k_best.transform(x_test)\n",
#     "    else:\n",
#     "        select_k_best.fit(x_main, y_train)\n",
#     "    \n",
#     "    selected_features_anova = itemgetter(*select_k_best.get_support(indices=True))(list_features)\n",
#     "    print(selected_features_anova)\n",
#     "    print(select_k_best.get_support(indices=True))\n",
#     "    print(\"****************************************\")\n",
#     "    \n",
#     "if selection_method == 'mutual_info' or selection_method == 'all':\n",
#     "    select_k_best = SelectKBest(mutual_info_classif, k=topk)\n",
#     "    if selection_method != 'all':\n",
#     "        x_train = select_k_best.fit_transform(x_main, y_train)\n",
#     "        x_cv = select_k_best.transform(x_cv)\n",
#     "        x_test = select_k_best.transform(x_test)\n",
#     "    else:\n",
#     "        select_k_best.fit(x_main, y_train)\n",
#     "\n",
#     "    selected_features_mic = itemgetter(*select_k_best.get_support(indices=True))(list_features)\n",
#     "    print(len(selected_features_mic), selected_features_mic)\n",
#     "    print(select_k_best.get_support(indices=True))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "scrolled": true
#    },
#    "outputs": [],
#    "source": [
#     "if selection_method == 'all':\n",
#     "    common = list(set(selected_features_anova).intersection(selected_features_mic))\n",
#     "    print(\"common selected featues\", len(common), common)\n",
#     "    if len(common) < num_features:\n",
#     "        raise Exception('number of common features found {} < {} required features. Increase \"topk variable\"'.format(len(common), num_features))\n",
#     "    feat_idx = []\n",
#     "    for c in common:\n",
#     "        feat_idx.append(list_features.index(c))\n",
#     "    feat_idx = sorted(feat_idx[0:225])\n",
#     "    print(feat_idx)"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "if selection_method == 'all':\n",
#     "    x_train = x_train[:, feat_idx]\n",
#     "    x_cv = x_cv[:, feat_idx]\n",
#     "    x_test = x_test[:, feat_idx]\n",
#     "\n",
#     "print(\"Shape of x, y train/cv/test {} {} {} {} {} {}\".format(x_train.shape, \n",
#     "                                                             y_train.shape, x_cv.shape, y_cv.shape, x_test.shape, y_test.shape))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "_labels, _counts = np.unique(y_train, return_counts=True)\n",
#     "print(\"percentage of class 0 = {}, class 1 = {}\".format(_counts[0]/len(y_train) * 100, _counts[1]/len(y_train) * 100))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "from sklearn.utils.class_weight import compute_class_weight\n",
#     "import tensorflow as tf\n",
#     "from tensorflow.keras import backend as K\n",
#     "from tensorflow.keras.utils import get_custom_objects\n",
#     "\n",
#     "def get_sample_weights(y):\n",
#     "    \"\"\"\n",
#     "    calculate the sample weights based on class weights. Used for models with\n",
#     "    imbalanced data and one hot encoding prediction.\n",
#     "\n",
#     "    params:\n",
#     "        y: class labels as integers\n",
#     "    \"\"\"\n",
#     "\n",
#     "    y = y.astype(int)  # compute_class_weight needs int labels\n",
#     "    class_weights = compute_class_weight('balanced', np.unique(y), y)\n",
#     "    \n",
#     "    print(\"real class weights are {}\".format(class_weights), np.unique(y))\n",
#     "    print(\"value_counts\", np.unique(y, return_counts=True))\n",
#     "    sample_weights = y.copy().astype(float)\n",
#     "    for i in np.unique(y):\n",
#     "        sample_weights[sample_weights == i] = class_weights[i]  # if i == 2 else 0.8 * class_weights[i]\n",
#     "        # sample_weights = np.where(sample_weights == i, class_weights[int(i)], y_)\n",
#     "\n",
#     "    return sample_weights\n",
#     "\n",
#     "def reshape_as_image(x, img_width, img_height):\n",
#     "    x_temp = np.zeros((len(x), img_height, img_width))\n",
#     "    for i in range(x.shape[0]):\n",
#     "        # print(type(x), type(x_temp), x.shape)\n",
#     "        x_temp[i] = np.reshape(x[i], (img_height, img_width))\n",
#     "\n",
#     "    return x_temp\n",
#     "\n",
#     "def f1_weighted(y_true, y_pred):\n",
#     "    y_true_class = tf.math.argmax(y_true, axis=1, output_type=tf.dtypes.int32)\n",
#     "    y_pred_class = tf.math.argmax(y_pred, axis=1, output_type=tf.dtypes.int32)\n",
#     "    conf_mat = tf.math.confusion_matrix(y_true_class, y_pred_class)  # can use conf_mat[0, :], tf.slice()\n",
#     "    # precision = TP/TP+FP, recall = TP/TP+FN\n",
#     "    rows, cols = conf_mat.get_shape()\n",
#     "    size = y_true_class.get_shape()[0]\n",
#     "    precision = tf.constant([0, 0, 0])  # change this to use rows/cols as size\n",
#     "    recall = tf.constant([0, 0, 0])\n",
#     "    class_counts = tf.constant([0, 0, 0])\n",
#     "\n",
#     "    def get_precision(i, conf_mat):\n",
#     "        print(\"prec check\", conf_mat, conf_mat[i, i], tf.reduce_sum(conf_mat[:, i]))\n",
#     "        precision[i].assign(conf_mat[i, i] / tf.reduce_sum(conf_mat[:, i]))\n",
#     "        recall[i].assign(conf_mat[i, i] / tf.reduce_sum(conf_mat[i, :]))\n",
#     "        tf.add(i, 1)\n",
#     "        return i, conf_mat, precision, recall\n",
#     "\n",
#     "    def tf_count(i):\n",
#     "        elements_equal_to_value = tf.equal(y_true_class, i)\n",
#     "        as_ints = tf.cast(elements_equal_to_value, tf.int32)\n",
#     "        count = tf.reduce_sum(as_ints)\n",
#     "        class_counts[i].assign(count)\n",
#     "        tf.add(i, 1)\n",
#     "        return count\n",
#     "\n",
#     "    def condition(i, conf_mat):\n",
#     "        return tf.less(i, 3)\n",
#     "\n",
#     "    i = tf.constant(3)\n",
#     "    i, conf_mat = tf.while_loop(condition, get_precision, [i, conf_mat])\n",
#     "\n",
#     "    i = tf.constant(3)\n",
#     "    c = lambda i: tf.less(i, 3)\n",
#     "    b = tf_count(i)\n",
#     "    tf.while_loop(c, b, [i])\n",
#     "\n",
#     "    weights = tf.math.divide(class_counts, size)\n",
#     "    numerators = tf.math.multiply(tf.math.multiply(precision, recall), tf.constant(2))\n",
#     "    denominators = tf.math.add(precision, recall)\n",
#     "    f1s = tf.math.divide(numerators, denominators)\n",
#     "    weighted_f1 = tf.reduce_sum(f.math.multiply(f1s, weights))\n",
#     "    return weighted_f1\n",
#     "\n",
#     "def f1_metric(y_true, y_pred):\n",
#     "    \"\"\"\n",
#     "    this calculates precision & recall \n",
#     "    \"\"\"\n",
#     "\n",
#     "    def recall(y_true, y_pred):\n",
#     "        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))  # mistake: y_pred of 0.3 is also considered 1\n",
#     "        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))\n",
#     "        recall = true_positives / (possible_positives + K.epsilon())\n",
#     "        return recall\n",
#     "\n",
#     "    def precision(y_true, y_pred):\n",
#     "        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))\n",
#     "        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))\n",
#     "        precision = true_positives / (predicted_positives + K.epsilon())\n",
#     "        return precision\n",
#     "\n",
#     "    precision = precision(y_true, y_pred)\n",
#     "    recall = recall(y_true, y_pred)\n",
#     "    # y_true_class = tf.math.argmax(y_true, axis=1, output_type=tf.dtypes.int32)\n",
#     "    # y_pred_class = tf.math.argmax(y_pred, axis=1, output_type=tf.dtypes.int32)\n",
#     "    # conf_mat = tf.math.confusion_matrix(y_true_class, y_pred_class)\n",
#     "    # tf.Print(conf_mat, [conf_mat], \"confusion_matrix\")\n",
#     "\n",
#     "    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))\n",
#     "\n",
#     "get_custom_objects().update({\"f1_metric\": f1_metric, \"f1_weighted\": f1_weighted})"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "scrolled": true
#    },
#    "outputs": [],
#    "source": [
#     "sample_weights = get_sample_weights(y_train)\n",
#     "print(\"Test sample_weights\")\n",
#     "rand_idx = np.random.randint(0, 1000, 30)\n",
#     "print(y_train[rand_idx])\n",
#     "print(sample_weights[rand_idx])"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "one_hot_enc = OneHotEncoder(sparse=False, categories='auto')  # , categories='auto'\n",
#     "y_train = one_hot_enc.fit_transform(y_train.reshape(-1, 1))\n",
#     "print(\"y_train\",y_train.shape)\n",
#     "y_cv = one_hot_enc.transform(y_cv.reshape(-1, 1))\n",
#     "y_test = one_hot_enc.transform(y_test.reshape(-1, 1))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "dim = int(np.sqrt(num_features))\n",
#     "x_train = reshape_as_image(x_train, dim, dim)\n",
#     "x_cv = reshape_as_image(x_cv, dim, dim)\n",
#     "x_test = reshape_as_image(x_test, dim, dim)\n",
#     "# adding a 1-dim for channels (3)\n",
#     "x_train = np.stack((x_train,) * 3, axis=-1)\n",
#     "x_test = np.stack((x_test,) * 3, axis=-1)\n",
#     "x_cv = np.stack((x_cv,) * 3, axis=-1)\n",
#     "print(\"final shape of x, y train/test {} {} {} {}\".format(x_train.shape, y_train.shape, x_test.shape, y_test.shape))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "from matplotlib import pyplot as plt\n",
#     "%matplotlib inline\n",
#     "\n",
#     "fig = plt.figure(figsize=(15, 15))\n",
#     "columns = rows = 3\n",
#     "for i in range(1, columns*rows +1):\n",
#     "    index = np.random.randint(len(x_train))\n",
#     "    img = x_train[index]\n",
#     "    fig.add_subplot(rows, columns, i)\n",
#     "    plt.axis(\"off\")\n",
#     "    plt.title('image_'+str(index)+'_class_'+str(np.argmax(y_train[index])), fontsize=10)\n",
#     "    plt.subplots_adjust(wspace=0.2, hspace=0.2)\n",
#     "    plt.imshow(img)\n",
#     "plt.show()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "from tensorflow.keras.models import Sequential, load_model, Model\n",
#     "from tensorflow.keras.layers import Dense, Dropout\n",
#     "from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, LeakyReLU\n",
#     "from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger, Callback\n",
#     "from tensorflow.keras import optimizers\n",
#     "from tensorflow.keras.regularizers import l2, l1, l1_l2\n",
#     "from tensorflow.keras.initializers import RandomUniform, RandomNormal\n",
#     "from tensorflow.keras.models import load_model\n",
#     "from tensorflow.keras import regularizers\n",
#     "\n",
#     "params = {'batch_size': 80, 'conv2d_layers': {'conv2d_do_1': 0.2, 'conv2d_filters_1': 32, 'conv2d_kernel_size_1': 3, 'conv2d_mp_1': 0, \n",
#     "                                               'conv2d_strides_1': 1, 'kernel_regularizer_1': 0.0, 'conv2d_do_2': 0.3, \n",
#     "                                               'conv2d_filters_2': 64, 'conv2d_kernel_size_2': 3, 'conv2d_mp_2': 2, 'conv2d_strides_2': 1, \n",
#     "                                               'kernel_regularizer_2': 0.0, 'layers': 'two'}, \n",
#     "           'dense_layers': {'dense_do_1': 0.3, 'dense_nodes_1': 128, 'kernel_regularizer_1': 0.0, 'layers': 'one'},\n",
#     "           'epochs': 3000, 'lr': 0.001, 'optimizer': 'adam'}\n"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "from functools import *\n",
#     "from sklearn.metrics import f1_score\n",
#     "from tensorflow.keras.metrics import AUC\n",
#     "\n",
#     "def f1_custom(y_true, y_pred):\n",
#     "    y_t = np.argmax(y_true, axis=1)\n",
#     "    y_p = np.argmax(y_pred, axis=1)\n",
#     "    f1_score(y_t, y_p, labels=None, average='weighted', sample_weight=None, zero_division='warn')\n",
#     "\n",
#     "def create_model_cnn(params):\n",
#     "    model = Sequential()\n",
#     "\n",
#     "    print(\"Training with params {}\".format(params))\n",
#     "    \n",
#     "    conv2d_layer1 = Conv2D(params[\"conv2d_layers\"][\"conv2d_filters_1\"],\n",
#     "                           params[\"conv2d_layers\"][\"conv2d_kernel_size_1\"],\n",
#     "                           strides=params[\"conv2d_layers\"][\"conv2d_strides_1\"],\n",
#     "                           kernel_regularizer=regularizers.l2(params[\"conv2d_layers\"][\"kernel_regularizer_1\"]), \n",
#     "                           padding='same',activation=\"relu\", use_bias=True,\n",
#     "                           kernel_initializer='glorot_uniform',\n",
#     "                           input_shape=(x_train[0].shape[0],\n",
#     "                                        x_train[0].shape[1], x_train[0].shape[2]))\n",
#     "    model.add(conv2d_layer1)\n",
#     "    if params[\"conv2d_layers\"]['conv2d_mp_1'] > 1:\n",
#     "        model.add(MaxPool2D(pool_size=params[\"conv2d_layers\"]['conv2d_mp_1']))\n",
#     "        \n",
#     "    model.add(Dropout(params['conv2d_layers']['conv2d_do_1']))\n",
#     "    if params[\"conv2d_layers\"]['layers'] == 'two':\n",
#     "        conv2d_layer2 = Conv2D(params[\"conv2d_layers\"][\"conv2d_filters_2\"],\n",
#     "                               params[\"conv2d_layers\"][\"conv2d_kernel_size_2\"],\n",
#     "                               strides=params[\"conv2d_layers\"][\"conv2d_strides_2\"],\n",
#     "                               kernel_regularizer=regularizers.l2(params[\"conv2d_layers\"][\"kernel_regularizer_2\"]),\n",
#     "                               padding='same',activation=\"relu\", use_bias=True,\n",
#     "                               kernel_initializer='glorot_uniform')\n",
#     "        model.add(conv2d_layer2)\n",
#     "        \n",
#     "        if params[\"conv2d_layers\"]['conv2d_mp_2'] > 1:\n",
#     "            model.add(MaxPool2D(pool_size=params[\"conv2d_layers\"]['conv2d_mp_2']))\n",
#     "        \n",
#     "        model.add(Dropout(params['conv2d_layers']['conv2d_do_2']))\n",
#     "\n",
#     "    model.add(Flatten())\n",
#     "\n",
#     "    model.add(Dense(params['dense_layers'][\"dense_nodes_1\"], activation='relu'))\n",
#     "    model.add(Dropout(params['dense_layers']['dense_do_1']))\n",
#     "\n",
#     "    if params['dense_layers'][\"layers\"] == 'two':\n",
#     "        model.add(Dense(params['dense_layers'][\"dense_nodes_2\"], activation='relu', \n",
#     "                        kernel_regularizer=params['dense_layers'][\"kernel_regularizer_1\"]))\n",
#     "        model.add(Dropout(params['dense_layers']['dense_do_2']))\n",
#     "\n",
#     "    model.add(Dense(3, activation='softmax'))\n",
#     "    \n",
#     "    if params[\"optimizer\"] == 'rmsprop':\n",
#     "        optimizer = optimizers.RMSprop(lr=params[\"lr\"])\n",
#     "    elif params[\"optimizer\"] == 'sgd':\n",
#     "        optimizer = optimizers.SGD(lr=params[\"lr\"], decay=1e-6, momentum=0.9, nesterov=True)\n",
#     "    elif params[\"optimizer\"] == 'adam':\n",
#     "        optimizer = optimizers.Adam(learning_rate=params[\"lr\"], beta_1=0.9, beta_2=0.999, amsgrad=False)\n",
#     "    \n",
#     "    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy', f1_metric])\n",
#     "    \n",
#     "    return model\n",
#     "\n",
#     "def check_baseline(pred, y_test):\n",
#     "    print(\"size of test set\", len(y_test))\n",
#     "    e = np.equal(pred, y_test)\n",
#     "    print(\"TP class counts\", np.unique(y_test[e], return_counts=True))\n",
#     "    print(\"True class counts\", np.unique(y_test, return_counts=True))\n",
#     "    print(\"Pred class counts\", np.unique(pred, return_counts=True))\n",
#     "    holds = np.unique(y_test, return_counts=True)[1][2]  # number 'hold' predictions\n",
#     "    print(\"baseline acc:\", (holds/len(y_test)*100))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "scrolled": false
#    },
#    "outputs": [],
#    "source": [
#     "from IPython.display import SVG\n",
#     "from tensorflow.keras.utils import plot_model\n",
#     "from keras.utils.vis_utils import model_to_dot\n",
#     "\n",
#     "model = create_model_cnn(params)\n",
#     "plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=False)\n",
#     "\n",
#     "# SVG(model_to_dot(model).create(prog='dot', format='svg'))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "import os\n",
#     "\n",
#     "best_model_path = os.path.join('.', 'best_model_keras')\n",
#     "es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,\n",
#     "                   patience=100, min_delta=0.0001)\n",
#     "# csv_logger = CSVLogger(os.path.join(OUTPUT_PATH, 'log_training_batch.log'), append=True)\n",
#     "rlp = ReduceLROnPlateau(monitor='val_loss', factor=0.02, patience=20, verbose=1, mode='min',\n",
#     "                        min_delta=0.001, cooldown=1, min_lr=0.0001)\n",
#     "mcp = ModelCheckpoint(best_model_path, monitor='val_f1_metric', verbose=1,\n",
#     "                      save_best_only=True, save_weights_only=False, mode='max', period=1)  # val_f1_metric"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "%%time\n",
#     "history = model.fit(x_train, y_train, epochs=params['epochs'], verbose=1,\n",
#     "                            batch_size=64, shuffle=True,\n",
#     "                            # validation_split=0.3,\n",
#     "                            validation_data=(x_cv, y_cv),\n",
#     "                            callbacks=[mcp, rlp, es]\n",
#     "                            , sample_weight=sample_weights)"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "scrolled": true
#    },
#    "outputs": [],
#    "source": [
#     "from matplotlib import pyplot as plt\n",
#     "%matplotlib inline\n",
#     "InteractiveShell.ast_node_interactivity = \"last\"\n",
#     "\n",
#     "plt.figure()\n",
#     "plt.plot(history.history['loss'])\n",
#     "plt.plot(history.history['val_loss'])\n",
#     "plt.plot(history.history['f1_metric'])\n",
#     "plt.plot(history.history['val_f1_metric'])\n",
#     "\n",
#     "plt.title('Model loss')\n",
#     "plt.ylabel('Loss')\n",
#     "plt.xlabel('Epoch')\n",
#     "plt.legend(['train_loss', 'val_loss', 'f1', 'val_f1'], loc='upper left')\n",
#     "plt.show()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "scrolled": true
#    },
#    "outputs": [],
#    "source": [
#     "from sklearn.metrics import confusion_matrix, roc_auc_score, cohen_kappa_score\n",
#     "import seaborn as sns\n",
#     "\n",
#     "model = load_model(best_model_path)\n",
#     "test_res = model.evaluate(x_test, y_test, verbose=0)\n",
#     "print(\"keras evaluate=\", test_res)\n",
#     "pred = model.predict(x_test)\n",
#     "pred_classes = np.argmax(pred, axis=1)\n",
#     "y_test_classes = np.argmax(y_test, axis=1)\n",
#     "check_baseline(pred_classes, y_test_classes)\n",
#     "conf_mat = confusion_matrix(y_test_classes, pred_classes)\n",
#     "print(conf_mat)\n",
#     "labels = [0,1,2]\n",
#     "\n",
#     "f1_weighted = f1_score(y_test_classes, pred_classes, labels=None, \n",
#     "         average='weighted', sample_weight=None)\n",
#     "print(\"F1 score (weighted)\", f1_weighted)\n",
#     "print(\"F1 score (macro)\", f1_score(y_test_classes, pred_classes, labels=None, \n",
#     "         average='macro', sample_weight=None))\n",
#     "print(\"F1 score (micro)\", f1_score(y_test_classes, pred_classes, labels=None, \n",
#     "         average='micro', sample_weight=None))  # weighted and micro preferred in case of imbalance\n",
#     "\n",
#     "# https://scikit-learn.org/stable/modules/model_evaluation.html#cohen-s-kappa --> supports multiclass; ref: https://stats.stackexchange.com/questions/82162/cohens-kappa-in-plain-english\n",
#     "print(\"cohen's Kappa\", cohen_kappa_score(y_test_classes, pred_classes))\n",
#     "\n",
#     "recall = []\n",
#     "for i, row in enumerate(conf_mat):\n",
#     "    recall.append(np.round(row[i]/np.sum(row), 2))\n",
#     "    print(\"Recall of class {} = {}\".format(i, recall[i]))\n",
#     "print(\"Recall avg\", sum(recall)/len(recall))"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "# !conda uninstall pydot\n",
#     "# !conda uninstall pydotplus\n",
#     "# !conda uninstall graphviz\n",
#     "\n",
#     "!conda install pydot\n",
#     "!conda install pydotplus"
#    ]
#   }
#  ],
#  "metadata": {
#   "kernelspec": {
#    "display_name": "Python 3",
#    "language": "python",
#    "name": "python3"
#   },
#   "language_info": {
#    "codemirror_mode": {
#     "name": "ipython",
#     "version": 3
#    },
#    "file_extension": ".py",
#    "mimetype": "text/x-python",
#    "name": "python",
#    "nbconvert_exporter": "python",
#    "pygments_lexer": "ipython3",
#    "version": "3.7.6"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 1
# }