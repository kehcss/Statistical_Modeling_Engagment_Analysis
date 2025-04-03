#Factor analysis for motivational_dataset.

# load packages -----

library(haven)      # read in stata data
library(vtable)     # summary tables
library(labelled)   # to see and create variable labels
library(tidyverse)  # data processing
library(psych)             # Load the package
library(readxl)
library(grid)
library(REdaS)
library(paran)
library(car)
# load motivation survey data -----
survey <- read_excel("survey_data.xlsx")

# Check new dimensions of the survey
dim(survey)

# Select relevant variables
data <- survey[, c("baseline_how_much_like_math",	"baseline_confidence_in_math_skills_abilities", "baseline_comfortable_participating_in_math_class",	"baseline_enjoy_mathematical_challenges",	"baseline_math_relationship_average_rating", "mid_year_how_much_like_math",	"mid_year_confidence_in_math_skills_abilities",	"mid_year_comfortable_participating_in_math_class",	"mid_year_enjoy_mathematical_challenges",	"mid_year_math_relationship_average_rating", "mid_year_relationship_with_tutor", "final_how_much_like_math", "final_confidence_in_math_skills_abilities", "final_comfortable_participating_in_math_class", "final_enjoy_mathematical_challenges", "final_math_relationship_average_rating",	"final_relationship_with_tutor")]  

# Drop columns with missing data
data <- data %>% drop_na()

# Check new dimensions of the dataset
dim(data)  # Returns number of rows and columns

#Calculate a correlation matrix
cor_matrix <- cor(data)

# Convert the correlation matrix to a dataframe
cor_df <- as.data.frame(cor_matrix)

write.csv(cor_df, "correlation_matrix.csv")

#Print
print(cor_matrix)

#Test for sampling adequacy (KMO):
KMO(data)

#Check Bartlett's test of sphericity:
cortest.bartlett(data, n = nrow(data))

#Factor analysis:
fa(data, nfactors = 17, rotate = "oblimin")

#Select SS loading > 1. analysis:
fa(data, nfactors = 13, rotate = "oblimin")

#Plot and visualize
M1<- fa(data, nfactors = 13, rotate = "oblimin")
fa.diagram(M1, main = "data")



#Paralle Analysis
paran(data, cfa=TRUE, graph=TRUE, color=TRUE, col=c("black", "red", "blue"))


#Bobby code to using 4 factors and save as csv
fa1 <- fa(data, nfactors = 4, rotate = "promax")
print(fa1, sort = TRUE, cut = .4)
preds <- factor.scores(survey[,-c(1:4)],fa1, missing = TRUE)
write.csv(preds$scores, "FactorScores.csv", row.names = FALSE)

#Plot and visualize
#M2<- fa(data, nfactors = 6, rotate = "oblimin")
#fa.diagram(M2, main = "data")

dat2 <- data
#dat2 <- apply(dat2. 2, function(x) ifelse(is.na(x). mean(x, na.rm = TRUE), x))









#Other test cases given issue of signluarlity
# Ensure data is numeric
data <- data %>% select_if(is.numeric)

# Calculate correlation matrix
cor_matrix <- cor(data, use = "pairwise.complete.obs")

# Check determinant
determinant <- det(cor_matrix)
print(determinant)

# Proceed with KMO if determinant is not too small
if (determinant > 1e-10) {
  kmo_result <- KMO(cor_matrix)
  print(kmo_result)
} else {
  print("Correlation matrix is singular. Consider reducing multicollinearity or removing highly correlated variables.")
}




# Compute VIF for the dataset
# Create a linear model (you can use any variable as the dependent variable)
vif_model <- lm(baseline_how_much_like_math, data = data)  # Replace with an actual dependent variable
vif_values <- vif(vif_model)

# Display VIF values
print(vif_values)

# Identify variables with high VIF (e.g., > 5)
high_vif_vars <- names(vif_values[vif_values > 5])
print(high_vif_vars)



