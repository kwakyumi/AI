# -*- coding: utf-8 -*-
"""과제_반도체 공정 데이터를 활용한 공정 이상 예측

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rbyPOxovZJnj2n_FPNwaqFCZ79g1BwXa

# [AI 프로젝트] 반도체 공정 이상 예측

---

## 프로젝트 목표
- 반도체 공정 데이터 분석을 통하여 공정 이상을 예측하는 분류 모델 수행
- 공정 이상에 영향을 미치는 요소들에 대한 데이터 분석

---

## 프로젝트 목차

1. **데이터 읽기:** 반도체 공정(SECOM) 데이터를 불러오고 Dataframe 구조를 확인<br>


2. **데이터 정제:** 결측치 또는 이상치 대체<br>


3. **데이터 시각화:** 변수 시각화를 통하여 분포 파악<br>
    3.1. Pass/Fail 시각화<br>
    3.2. 센서 데이터 시각화 하기<br>
    3.3. 중요한 변수 찾기<br>
    3.4. 59번 센서 데이터 시각화 하기<br>


4. **데이터 전처리:** 머신러닝 모델에 필요한 입력값 형식으로 데이터 처리<br>
    4.1. x와 y로 분리<br>
    4.2. 데이터 정규화<br>


5. **인공지능 모델 학습:** 분류 모델을 사용하여 학습 수행<br>
    5.1. 기본 분류 모델 학습 - 로지스틱 분류기<br>
    5.2. 다양한 분류 모델 학습<br>


6. **평가 및 예측:** 학습된 모델을 바탕으로 평가 및 예측 수행<br>
    6.1. Confusion Matrix(오차행렬)<br>
    6.2. Precision & Recall(정밀도&재현율)<br>
    6.3. 테스트 데이터의 예측값 출력<br>

---

## 데이터 출처
- https://archive.ics.uci.edu/ml/datasets/SECOM

---

## 1. 데이터 읽기

pandas를 사용하여 `uci-secom.csv` 데이터를 읽고 dataframe 형태로 저장합니다.
"""

# numpy, pandas, matplotlib.pyplot, seaborn 패키지 설치
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# 데이터를 불러오는 다양한 방법
# data = pd.read_csv('https://archive.ics.uci.edu/ml/datasets/SECOM')
# data = pd.read_csv('https://drive.google.com/file/d/14zNky3L_f-RsKHl31iYNgwfH0KG5Lz6U/view?usp=share_link')
# data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/AI project/P3/p3_uci-secom.csv')
# data = pd.read_csv('/p3_uci-secom.csv')

# 구글 드라이브에 있는 파일을 불러오기
# 구글 드라이브에 접속하고 로그인하여 my drive에 접근, 기본 디렉토리는 my drive(./)

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# 프로젝트 폴더 안의 파일 위치를 확인
# %cd /content/gdrive/My\ Drive/Colab Notebooks/AI project/P3

# uci-secom.csv 데이터를 pandas를 사용하여 dataframe 형태로 불러오기
# unicode 에러 방지, encoding = 'cp949' 또는 encoding = 'utf-8' 사용

data = pd.read_csv('./uci-secom.csv', encoding = 'utf-8')

# head()를 사용하여 5개의 행을 확인 (디폴트 값은 5개)
# head() 안에 숫자를 넣을 경우, 해당 숫자만큼 행을 확인 가능

data.head()

#10개의 행을 확인
data.head(10)

# 불러온 데이터의 dataframe의 정보를 요약해서 출력
# info()로 컬럼 이름, 결측값 등을 제외한 데이터의 정보를 확인
# shape로 데이터의 모양 확인, 1567 행, 592 열로 구성된 데이터
data.info()
data.shape

# describe() 함수는 수치형 변수의 데이터 정보를 요약하여 출력
# 총 592개의 변수 중 수치형 변수는 591개임을 확인
# count:컬럼 별 총 데이터 수
# mean: 평균
# std: 표준편차
# min: 최솟값
# max: 최댓값
# n-percentile분포도: 각 25%, 50%, 75% 지점의 값(4분위)

data.describe()

"""## 2. 데이터 정제

일반적으로 데이터 정제 과정은 **결측값(missing value)** 또는 **이상치(outlier)**를 처리합니다.

**결측값**: 값이 없는 것, NaN, Null 등 

**이상치**: 일반적인 범주에서 벗어난 값.

(예시: 200살, -10살 등과 같이 일반적인 범주에 포함되지 않는 값)
"""

# 각 변수 별 결측값 정보를 출력
# isnull()은 결측값 여부를 True, False 값으로 반환
# True: 데이터 값이 없음(결측값)
# False: 정상적으로 값이 있음

data.isnull()

# data.isnull().sum()로 각 컬럼에서 결측값의 수 출력

# 출력 결과 읽는 방법
# Time 변수(세로, 열, 컬럼, 변수, 특성)에 결측값 0개, 0 변수에 결측값 6개

data.isnull().sum()

# data.isnull().sum().sum()로 전체 결측값의 수를 확인
data.isnull().sum().sum()

"""**결측값을 대체값으로 변환**

이상치 또는 결측치를 대체하는 방법은 주로 평균 대체, 중앙 대체, 빈도 대체, 더미 대체 등을 사용합니다.

결측값이 많지 않다면 fillna(값, inplace=True)를 사용하여 결측값이 존재하는 데이터(행)를 전체 삭제하는 방법도 있습니다.

그러나 이번에는 프로젝트에서는 데이터의 양이 적기 때문에 데이터 전체를 사용하기 위해 누락된 값(결측치)를 대표값 또는 더미값으로 변경하는 더미 대체 방법을 사용하겠습니다. (더미값은 주로 0을 사용함)
"""

# 결측값을 0으로 대체

# DataFrame.fillna(0, inplace=True)을 사용
# np.NaN 은 결측값, replace()을 사용해서 0으로 변경

data = data.replace(np.NaN, 0)

# 결측값이 대체값으로 잘 변경되었는지 확인
data.isnull().sum()

# 'Time'변수의 데이터는 pass/fail(공정 이상)을 예측하는데 큰 영향이 없는 변수로 판단 -> 삭제
# axis=0은 행 방향(가로)으로 동작
# axis=1은 열 방향(세로)으로 동작 

# drop() 안에 삭제할 컬럼 이름과 axis =1 (세로)를 작성
data = data.drop(columns = ['Time'], axis = 1)

data.shape

# data에서 time 변수가 삭제되었는지 확인
# Time이 삭제된 것을 확인
data

"""## 3. 데이터 시각화

머신러닝 데이터에서 숫자만으로는 데이터가 어떤 의미를 가지는지 파악하기 어렵습니다. 중요한 변수를 알지 못해 찾아야하는 경우(중요 변수의 목록/후보가 없는 경우) 전체 변수를 시각화하여 변수의 현황을 파악하고 중요 변수를 찾는 과정이 선행되어야 합니다.

각 변수 분포를 알아보기 위하여 **데이터를 시각화**를 수행하겠습니다.

센서에 관련된 591개의 변수들을 모두 시각화하기에는 너무 양이 많기때문에 나눠서 출력하고, 이후 영향력이 크다고 판단되는 변수를 예시로 출력합니다.

이번에는 중요도가 높은 변수인 `59` 센서에 대해서만 대표로 시각화를 진행하도록 하겠습니다.

### 3.1. `Pass/Fail` 시각화
"""

# 전체 1567개(가로 행 데이터)의 값에서 정상제품(-1)은 1463개, 이상제품(1)은 104개

# 막대 그래프를 사용하여 정상제품(-1)과 이상제품(1)의 분포 출력
# pandas 모듈을 plot()를 사용해서 막대그래프 출력
# value_counts()로 합계 출력
data['Pass/Fail'].value_counts().plot(kind='bar')

# 도수분포표로 분포 확인.
data['Pass/Fail'].value_counts()

"""### 3.2. 센서 데이터 시각화 하기

다수의 feature 데이터에 대해서 한눈에 볼 수 있도록 시각화를 수행할 때는 seaborn의 `pairplot`를 활용하면 좋습니다. 

`pairplot`으로  전체 591개 센서에 대한 출력을 수행하기 어렵기 때문에 0~4, Pass/Fail 데이터로 data_test를 만들어 시각화 하는 방법을 보여드리겠습니다.

(1) 데이터 시각화를 위한 리스트 변수 만들기
"""

# (1) 데이터 시각화를 위한 리스트 변수 만들기_1

# 0,1,2,3,4,Pass/Fail 6개의 컬럼(세로 열)으로 새로운 DataFrame을 만들기
# 리스트 안에 출력할 컬럼 이름을 작성 

data_test= data[['0','1','2','3','4','Pass/Fail']]
data_test

# (1) 데이터 시각화를 위한 리스트 변수 만들기_2.1

# feature는 591개의 센서 값(세로 열)에 해당
# 데이터의 변수 이름이 규칙성 있는 일련의 숫자인 경우 반복문을 사용하여 간소화 가능
# 만약 규칙성이 없는 변수명을 가진 경우, 희망하는 변수명을 직접 리스트에 작성해서 만들어야 함

feature = [ str(x) for x in range(0,590)] + ['Pass/Fail']
print(data[feature])

# (1) 데이터 시각화를 위한 리스트 변수 만들기_2.2

# 데이터 프레임 변수 만들기

feature = data[[ str(x) for x in range(0,590)] + ['Pass/Fail']]
print(feature)

"""(2) 데이터 시각화_표 출력"""

# 데이터 출력_전체 행 출력
pd.set_option('display.max_rows', None)
print(data_test)

# 데이터 출력_전체 열 출력
pd.set_option('display.max_columns', None)
print(data_test)

# 데이터 출력_전체 행, 열 출력 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(data_test)

"""(3) 데이터 시각화_그래프 출력"""

#seaborn의 pairplot()을 사용해서 컬럼끼리 비교 
sns.pairplot(data_test)

# vars를 사용해서 특정한 컬럼끼리 비교(1)
sns.pairplot(data_test,height=5, vars=['3','4'])

# vars를 사용해서 특정한 컬럼끼리 비교(2)
sns.pairplot(data_test,height=5, vars=['1','3','4'])

"""### 3.3. 중요한 변수 도출하기

**SHAP** 모델을 사용하여 중요한 변수를 확인하겠습니다.

**Shap Value**

 공정 분배 게임 이론을 기반으로 게임에 참여한 참여자들에게 상금을 공정하게 배분하는 하나의 방법

**SHAP(SHapley Additive exPlanation)**

Shap Value를 머신러닝 모델의 조건부 기댓값 함수를 이용하여 구하고, 데이터셋에서 전역(global) 변수의 중요도 및 개별 예측값에 대한 각 변수들의 영향력을 클래스에 상관없이(Model-Agnostic) Additive하게 배분하는 방식 

- 모델에 특정 변수가 있는 경우와 없는 경우를 나누어 변수의 중요도(영향력)를 계산

- 변수를 보는 순서에 영향을 받지 않도록 가능한 모든 순서로 비교하여 공정하게 변수의 중요도를 측정
"""

#중요한 변수를 찾는 방법, Shap Value 사용
# 데이터 shape 파악
nCar = data.shape[0] # 데이터 개수
nVar = data.shape[1] # 변수 개수
print('nCar: %d' % nCar, 'nVar: %d' % nVar )

# Pass/Fail-target, 그 외 feature을 x와 y로 분리
feature_columns = list(data.columns.difference(['Pass/Fail'])) 
X = data[feature_columns]
y = data['Pass/Fail']

# train/test 비율을 7:3으로 설정
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size = 0.3, random_state = 42) 

# train/test 데이터 확인
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

# lightgbm을 구현하여 shap value를 예측
# Decision Tree 기반의 Ensemble모형을 구현
# lightGBM모델로 boosting(Gradient Boosting)의 방법 중 하나

# library
import lightgbm as lgb  # 없을 경우 cmd/anaconda prompt에서 install
from math import sqrt
from sklearn.metrics import mean_squared_error

# lightgbm model
# LightGBM 모델에 맞게 변환
lgb_dtrain = lgb.Dataset(data = train_x, label = train_y) 
lgb_param = {'max_depth': 10,
            'learning_rate': 0.01, # Step Size
            'n_estimators': 1000, # Number of trees
            'objective': 'regression'} # 목적 함수 (L2 Loss)
lgb_model = lgb.train(params = lgb_param, train_set = lgb_dtrain) # 학습 진행
lgb_model_predict = lgb_model.predict(test_x) # test data 예측
print("RMSE: {}".format(sqrt(mean_squared_error(lgb_model_predict, test_y)))) # RMSE

# shap value를 이용하여 각 변수의 영향도 파악

# !pip install shap (에러 발생시, skimage version 확인 (0.14.2 이상 권장))
# import skimage -> skimage.__version__ (skimage version 확인)
# skimage version upgrade -> !pip install --upgrade scikit-image

!pip install shap
import skimage

# shap value 
import shap
explainer = shap.TreeExplainer(lgb_model) # Tree model Shap Value 확인 객체 지정
shap_values = explainer.shap_values(test_x) # Shap Values 계산

# version 확인
import skimage
skimage.__version__

shap.initjs() # javascript 초기화 (graph 초기화)

# 1번째 test data instance에 대해 Shap Value를 적용하여 시각화
# 예측값에 긍정적(양의 영향력)은 빨간색, 부정적(음의 영향력)은 파란색
# bar의 크기가 영향의 크기를 의미함

shap.force_plot(explainer.expected_value, shap_values[1,:], test_x.iloc[1,:])

shap.initjs()

# 10번째 test data instance에 대해 Shap Value를 적용하여 시각화
shap.force_plot(explainer.expected_value, shap_values[10,:], test_x.iloc[10,:])

shap.initjs()

# 100번째 test data instance에 대해 Shap Value를 적용하여 시각화
shap.force_plot(explainer.expected_value, shap_values[100,:], test_x.iloc[100,:])

# 각 변수에 대한 |Shap Values|을 통해 변수의 전역 중요도(Global importance) 파악
 # 각 변수의 shap value에 절대값을 취한 것으로 변수의 평균적인 영향력을 보여줌 
 # 큰 영향력을 보일수록, target(Pass/Fail)과 관계성이 크다는 것을 의미함 
 # 이는 변수의 중요도와 비슷한 개념이나 인과관계를 의미하는 것은 아님

shap.summary_plot(shap_values, test_x, plot_type = "bar")

# summary
# 변수들의 shap value를 요약
# 해당 변수가 빨간색을 띄면 target(Pass/Fail)에 대해 양의 영향력, 파란색을 띄면 음의 영향력

# 해석1: 59번 센서의 값이 높을수록 Pass/Fail이 높은 경향성이 있다.
# 해석2: 488번 센서의 값이 낮을수록 Pass/Fail이 높은 경향성이 있다.
# 해석3: 150, 82번 센서는 해석이 모호함, Feature Value에 따른 Shap Values의 상관성 파악 모호

shap.summary_plot(shap_values, test_x)

"""### 3.4. `59`번 센서 시각화"""

# subplots는 한 번에 여러 그래프를 보여주기 위해서 사용 
# subplots()에서 figure와 axes 두개의 값을 받을 수 있음 
# 이때 변수명은 상관없으나 순서가 중요

# fig는 figure로써 전체 subplot, ax는 axe로써 각각의 그래프를 의미
# figsize(가로, 세로)로 그래프의 사이즈 설정
fig, ax = plt.subplots(figsize=(8, 6))

# seborn 그래프의 스타일을 darkgrid로 설정
# style에 white, whitegrid, dark 등을 넣어서 스타일 변경 가능
sns.set(style='darkgrid')


# displot로 59번 센서의 분포도 출력
# yellow, green와 같은 그래프 색깔 지정
sns.distplot(data['59'], color = 'darkblue')

# 그래프 제목, 폰트 크기 설정
plt.title('59 Sensor Measurements', fontsize = 20)

# 그래프의 사이즈를 설정
# 첫번째는 가로, 두번째는 세로의 크기
plt.rcParams['figure.figsize'] = (10, 16)

# 3x1 형태로 그래프를 출력하기 위하여 subplot을 설정 
# subplot(행, 열, 인덱스)로 그래프의 위치 지정 
plt.subplot(3, 1, 1)
sns.distplot(data['59'], color = 'darkblue')
plt.title('59 Sensor Measurements', fontsize = 20)

# 'Pass/Fail' 값이 1인 데이터를 출력
#  data[data['Pass/Fail']==1]를 하면 'Pass/Fail' 값이 1인 행만 사용할 수 있음
plt.subplot(3, 1, 2)
sns.distplot(data[data['Pass/Fail']==1]['59'], color = 'darkgreen')
plt.title('59 Sensor Measurements', fontsize = 20)

# 'Pass/Fail' 값이 -1인 데이터를 출력
plt.subplot(3, 1, 3)
sns.distplot(data[data['Pass/Fail']==-1]['59'], color = 'red')
plt.title('59 Sensor Measurements', fontsize = 20)

# 그래프의 사이즈를 설정
# 첫번째는 가로, 두번째는 세로의 크기
plt.rcParams['figure.figsize'] = (15, 10)

# 위에서 나누어 출력 했던 그래프를 한번에 출력
sns.distplot(data['59'], color = 'darkblue')
sns.distplot(data[data['Pass/Fail']==1]['59'], color = 'darkgreen')
sns.distplot(data[data['Pass/Fail']==-1]['59'], color = 'red')

# 그래프 제목, 폰트 크기 설정
plt.title('59 Sensor Measurements', fontsize = 20)

"""## 4. 데이터 전 처리

공정 이상 예측을 수행하기 위해서 주어진 센서 데이터(세로 열)에 대해서 분류 모델을 사용하겠습니다.

분류 모델의 필요한 입력 데이터를 준비 하기위해서 다음과 같은 전 처리를 수행합니다.

1. 전체 데이터를 feature 데이터인 `x`와 label 데이터인 `y`로 분리하기
2. StandardScaler를 사용하여여 데이터 표준화하기

### 4.1.  `x`와  `y`로 분리

머신러닝의 feature 데이터는 `x`, label 데이터는 `y`에 저장합니다.
"""

# 정답을 제거한 데이터 x
# 예측해야 할 변수인 `Pass/Fail`를 제거하여 머신러닝 입력값인 x에 저장
# data에는 'Pass/Fail'가 없어짐 
x = data.drop(columns = ['Pass/Fail'], axis = 1)

# 정답만 있는 데이터 y
# 예측해야 할 변수 `Pass/Fail`만을 선택하여 numpy 형태로 y에 저장
y = data['Pass/Fail']

# ravel은 "풀다"로 다차원을 1차원으로 푸는 것을 의미
# 1차원 벡터 형태로 출력하기 위해 ravel를 사용
y = y.to_numpy().ravel() 
y

# 타입을 확인
type(y)

"""원본 데이터의 수가 많지 않기에 원본 데이터에서 샘플 데이터를 추출하고 노이즈를 추가하여 테스트 데이터를 생성하였습니다.

`data` 폴더 내의 `uci-secom-test.csv`에 590개의 센서 데이터와 `Pass/Fail`저장되어 있기에 해당 데이터를 읽어와 `x_test, y_test` 데이터로 분리합니다.
"""

# 구글 드라이브 폴더 내의 uci-secom-test.csv를 DataFrame으로 읽고 x_test, y_test로 분리
data_test = pd.read_csv('./uci-secom-test.csv', encoding = 'utf-8')

x_test = data_test.drop(columns = ['Pass/Fail'], axis = 1)
y_test = data_test['Pass/Fail'].to_numpy().ravel()

# x_test 데이터 출력
x_test

"""### 4.2. 데이터 표준화

각 변수 마다의 스케일 차이를 맞추기 위하여 표준화를 수행합니다. 

표준화는 서로 다른 피처의 크기를 통일하기 위해서 크기를 변환해주는 개념입니다.

데이터의 피처 각각이 평균이 0이고 분산이 1인 가우시안 정규 분포를 형태와 가까워지도록 변환합니다.
"""

from sklearn.preprocessing import StandardScaler

# 정규화를 위해서 StandardScaler 불러옵니다.
sc = StandardScaler()

# x_train에 있는 데이터에 맞춰 정규화를 진행합니다. 
x_train = sc.fit_transform(x)
x_test = sc.transform(x_test)
y_train = y

#mean()으로 평균을 구하고 var()로 분산을 구합니다. 
#e는 소수부의 크기를 알려주는 자리입니다. 여기서는 엄청 작은 값으로 0으로 생각하면 됩니다. 
x_train_sc = pd.DataFrame(data=x_train)
print("평균")
print(x_train_sc.mean())
print("분산")
print(x_train_sc.var())

x_train_sc

"""## 5. 인공지능 모델 학습

전 처리된 데이터를 바탕으로 분류 모델 학습을 수행하고 학습 결과를 출력 해봅니다.

먼저 기본적인 분류 모델인 **로지스틱 분류기(logistic regression classifier)**를 사용하여 학습을 수행하고, 다양한 모델들을 적용해보겠습니다.

### 5.1. 기본 분류 모델 학습 - 로지스틱 분류기

### 로지스틱 회귀
로지스틱 회귀는 선형 회귀 방식을 분류에 적용한 알고리즘입니다. 

로지스틱 회귀는 이름에 회귀라는 말이 들어가지만 회귀 문제보다 주로 이진 분류(0,1)에 사용됩니다. 학습을 통해 시그모이드 함수 최적선을 찾고 이 시그모이드 함수의 반환 값을 확률로 간주해 확률에 따라 분류를 결정합니다. 예측 값은 예측 확률을 의미하며 예측 확률이 0.5이상이면 1로, 그렇지 않으면 0으로 예측합니다.
"""

# 로지스틱 분류기 모델
from sklearn.linear_model import LogisticRegression

# max_iter는 로지스틱 알고리즘의 반복 횟수를 정하는 파라미터
# default 값이 해당 프로젝트 값에 비해 부족하기 때문에 아래와 같이 설정
model = LogisticRegression(max_iter=5000)

# fit 함수를 사용하여 데이터를 학습 
model.fit(x_train, y_train)

# score 함수를 사용하여 모델의 성능 확인 
print(model.score(x_train, y_train))
print(model.score(x_test, y_test))

# Logistic Regression의 중요도를 계산
# 가중치 값들의 크기로 판단하여 .coef_로 해당 값들을 불러오기
abs_coef = np.abs(model.coef_).ravel()
abs_coef

# bar 형태 그래프로 Logistic Regression의 feature 별 중요도를 상위 30개 출력
# 상위 30개의 feature 정보를 출력하기 위하여 sorting을 수행하고 해당 feature 번호를 LR_imort_x에 저장
LR_import_x = [str(i[0]) for i in sorted(enumerate(abs_coef), key=lambda x:x[1], reverse=True)]

plt.bar(LR_import_x[:30], sorted(abs_coef, reverse=True)[:30])

plt.rcParams['figure.figsize'] = (10, 25)
plt.xlabel('Features')
plt.ylabel('Weight absolute values')
plt.show()

# sorted(abs_coef, reverse=True) 을 활용하면 쉽게 확인 가능
a=sorted(abs_coef,reverse=True)[0]
print(a)

"""### 5.2. 다양한 분류 모델 학습"""

#xgboost 설치가 잘 안되면 Anaconda Powershell Prompt(anaconda3)에서 시도
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import xgboost as xgb
from xgboost.sklearn import XGBClassifier


#여러 모델을 append해서 추가 
models = []
models.append(('LDA', LinearDiscriminantAnalysis()))  # LDA 모델
models.append(('KNN', KNeighborsClassifier()))  # KNN(K-최근접이웃) 모델
models.append(('CART', DecisionTreeClassifier()))  # 의사결정트리 모델
models.append(('NB', GaussianNB()))  # 가우시안 나이브 베이즈 모델
models.append(('RF', RandomForestClassifier()))  # 랜덤포레스트 모델
models.append(('SVM', SVC(gamma='auto')))  # SVM 모델
models.append(('XGB', XGBClassifier()))  # XGB 모델

for name, model in models:
    # fit으로 학습 수행
    model.fit(x_train, y_train)
    
    # %s와 %f는 문자열 포맷팅으로 %s는 문자열, %f는 숫자형 데이터 
    # 문자열 포맷팅 값은 괄호()안의 값과 대응
    # score 함수를 사용하여 모델의 성능을 확인
    msg = "%s - train_score : %f, test score : %f" % (name, model.score(x_train, y_train), model.score(x_test, y_test))
    print(msg)

# xgb 모델에서 변수 중요도를 출력
# xgboost 모듈의 plot_importance는 피처 중요도를 시각화할 때 사용 
# models[-1][1]는 models 리스트에서 맨 마지막 요소(이것도 리스트)에서 두번째 요소를 말합니다. 

# importance_type는 중요도가 어떻게 계산되는지 정함
# weight는 나온 횟수
# gain은 평균적인 이득
# cover는 coverage의 평균 

xgb.plot_importance(models[-1][1], height = 1, grid = True, importance_type = 'total_gain', show_values = False, max_num_features = 30)

plt.rcParams['figure.figsize'] = (10, 15)
plt.xlabel('The F-Score for each features')
plt.ylabel('Features')
plt.show()

"""## 6. 평가 및 예측

**머신러닝을 평가하는 다양한 방법**


1. 정확도 (Accuracy)
2. 오차행렬(Confusion Matrix)
3. 정밀도(Precision)
4. 재현율(Recall)
5. F1스코어
6. ROC AUC

---

학습 과정에서 학습 데이터와 테스트 데이터에 대해서 accuracy 계산하여 평가하였습니다.

accuracy의 경우 아래 식에서 알 수 있듯이 얼마나 정확히 예측했는가를 정량적으로 나타냅니다.

$Accuracy = \frac{Number \;of \;correct \;predictions}{Total \; number \;of \;predictions} $

Accuracy 값이 높으면 좋은 성능을 낸다고도 할 수 있지만 이번 실습인 공정 이상 예측에서는 recall 값 또한 살펴봐야 합니다.

오차행렬(Confusion Matrix)은 이진 분류의 예측 오류가 얼마인지와 더불어 어떠한 유형의 예측 오류가 발생하고 있는지를 함께 나타내는 지표입니다. 

+ TN : Negative(0)로 예측했고, 실제로도 True인 경우 - 실제는 Negative
+ FP : Positive(1)로 예측했지만 실제는 False인 경우 - 실제는 Negative
+ FN : Negative(0)로 예측했고, 실제는 False인 경우 - 실제는 Positive
+ TP : Positive(1)로 예측했고, 실제로도 True인 경우 - 실제는 Positive

공정 이상 예측에서 중요한 것은 이상 없음을 정확히 예측하는 것 보단 이상 있음을 정확히 예측하는 것입니다. 

recall 방식은 `예측한 이상 있음` 대비 `실제 이상 있음`의 비율을 나타내기에 accuracy에서 놓칠 수 있는 결과 해석을 보충합니다.

정밀도(Precision)는 예측을 Positve로 한 대상 중에 예측과 실제 값이 Positive로 일치한 데이터의 비율을 뜻합니다. 정밀도는 FP가 낮아야 합니다. 
+ TP / (FP + TP)

재현율(recall)은 실제 값이 Positive인 대상 중에 예측과 실제 값이 Positive로 일치한 데이터의 비율을 말합니다. 재현율은 FN이 낮아야 합니다.
+ TP / (FN + TP)


이번 파트에서는 recall 방식을 포함한 또 다른 대표적인 평가 방법에 대해서 알아보고 주어진 데이터에 대해서 예측하는 것을 수행해보겠습니다.

### 6.1. Confusion Matrix(오차행렬)

기존 score 결과는 accuracy 기반의 결과였습니다. confusion matrix를 출력하여 각 class 별로 예측한 결과에 대해서 확인합니다.
"""

from sklearn.metrics import confusion_matrix
import seaborn as sns 

# LinearDiscriminantAnalysis 모델의 confusion matrix를 사용하기 위하여 학습용 데이터의 예측값을 저장
# models[0]는 LDA
model_predition_train = models[0][1].predict(x_train)

# sklearn에서 제공하는 confusion_matrix를 사용
cm_train = confusion_matrix(y_train, model_predition_train)

# 출력 파트 - seaborn의 heatmap을 사용
plt.rcParams['figure.figsize'] = (5, 5)
sns.set(style = 'dark', font_scale = 1.4)

# annot은 annotate each cell with numeric value로 셀에 숫자값을 표시하는지 정하는 것
# cmap으로 색깔 지정 가능, cmap='RdYlGn_r' cmap="YlGnBu"
ax = sns.heatmap(cm_train, annot=True)
plt.xlabel('Prediction')
plt.ylabel('Real Data')
ax.set_xticklabels((-1,1))
ax.set_yticklabels((-1,1))
plt.show()
cm_train

"""위 confusion matrix에서 x 축은 실제 데이터의 label을 의미하고 y 축은 예측한 데이터의 label을 의미합니다.

- **0,0 의 값:** `이상 없음(Pass)` 이라고 예측했을 때, 실제 데이터가 `이상 없음(Pass)`인 경우의 개수
- **0,1 의 값:** `이상 있음(Fail)` 이라고 예측했을 때, 실제 데이터가 `이상 없음(Pass)`인 경우의 개수
- **1,0 의 값:** `이상 없음(Pass)` 이라고 예측했을 때, 실제 데이터가 `이상 있음(Fail)`인 경우의 개수
- **1,1 의 값:** `이상 있음(Fail)` 이라고 에측했을 때, 실제 데이터가 `이상 있음(Fail)`인 경우의 개수
"""

# LDA 모델에서 평가용 데이터(x_test, y_test)의 confusion matrix를 구하기
# LinearDiscriminantAnalysis의 x_test에 대한 예측값을 구하고 confusion_matrix() 를 사용
model_prediction_test=models[0][1].predict(x_test)
cm_test=confusion_matrix(y_test,model_prediction_test)

# confusion_matrix() 결과값을 저장 
cm_test

"""### 6.2. Precision & Recall(정밀도&재현율)

분류 모델의 또 다른 성능 지표로 Precsion과 Recall를 확인합니다.
"""

from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

# sklearn에서 제공하는 recall_score, precision_score를 사용하여 recall과 precision 결과 출력
print("Recall score: {}".format(recall_score(y_test, models[0][1].predict(x_test))))
print("Precision score: {}".format(precision_score(y_test, models[0][1].predict(x_test))))

"""### 6.3. 테스트 데이터의 예측값 출력"""

# 0번부터 29번까지 30개를 출력
for i in range(30): 
    
    # LDA 모델을 사용
    # reshape()에서 -1이 들어간 곳은 가변적으로 바꿉니다. 예를 들어 12개의 원소가 있고 reshape(-1,2)를 하면 열 2개를 맞추기 위해서 행을 6개로 바꿉니다. 
    prediction = models[0][1].predict(x_test[i].reshape(1,-1))
    
    #문자열 포맷팅의 방법입니다. {}가 괄호()안의 값에 각각 대응됩니다. 
    print("{} 번째 테스트 데이터의 예측 결과: {}, 실제 데이터: {}".format(i, prediction[0], y_test[i]))

"""---"""