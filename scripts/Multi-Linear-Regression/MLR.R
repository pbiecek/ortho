# Libraries
install.packages("readxl")
install.packages("car")
install.packages("lmtest")
install.packages("estimatr")
install.packages("moments") 
install.packages("sandwich") 
library(sandwich)
library(readxl)
library(car)  
library(lmtest)
library(estimatr)
library(moments)

# Load data
data <- read_excel("") #Enter the path of the data generated from Python preprocessing file

# Dummy variables transformation
data$Age_group <- as.factor(data$Age_group)  
data$track_level_1 <- as.factor(data$track_level_1)  
data$track_level_2 <- as.factor(data$track_level_2)  
data$track_level_3 <- as.factor(data$track_level_3)  

# Linear regression
formula <- time_spent_difficulty_3_first_success ~ Age_group + track_level_1 + track_level_2 + 
            track_level_3 + Level1_Count + Level2_Count + Level3_Incomplete_Count + 
            Level1_Time + Level2_Time + Level3_Incomplete_Time

model <- lm(formula, data = data)
summary(model)

# Multi-collinearity test
vif_values <- vif(model)
print(vif_values)

# Residual normality test
# Kolmogorov-Smirnov test (Residual normality test)
ks.test(residuals(model), "pnorm", mean = mean(residuals(model)), sd = sd(residuals(model))) #The residual is not normally distributed

skewness(residuals(model)) # Absolute value of skewness less than 3
kurtosis(residuals(model)) # Absolute value of excess kurtosis less than 10
hist(residuals(model)) # Based on skewness, kurtosis and the histogram, the residual is closed to normal distribution.

# Heteroscedasticity test
# BP test for heteroscedasticity
bptest_result <- bptest(model) #It does has heteroscedasticity, so robust standard error will be applied
print(bptest_result)

# OLS with robust standard errors
robust <- estimatr::lm_robust(formula, data = data, se_type = "HC1") 
robust

# Autocorrelation test
# Durbin-Watson Test 
dw_test <- dwtest(model)
print(dw_test)



