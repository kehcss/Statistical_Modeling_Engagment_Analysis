#Created: 09nov2022
#Updated: 01nov2024
#Ben Shear

# Overview -----

# script file to clean and merge SEDA 2022 data with data hub remote learning
# updating in November 2024 with the latest version of SEDA and Datahub data

# Directory and workspace -----

# use the Session> menu to setwd() to current location
# I usually run this first to make sure workspace is clear

rm(list=ls())

# load packages -----

library(haven)      # read in stata data
library(vtable)     # summary tables
library(labelled)   # to see and create variable labels
library(tidyverse)  # data processing

# load SEDA test score data -----

# FROM: https://edopportunity.org
# NOTE: if you want to use these data, please fill out the data use agreement
# at: https://edopportunity.org/get-the-data/

seda <- read_dta(file = "seda2022_admindist_poolsub_gys_2.0.dta")

# load data about remote learning -----
# FROM: https://www.covidschooldatahub.com/data-resources
# Reports the share of the 2020-21 school year that districts spent in different
# learning modes (in person, hybrid, or virtual).

datahub <- read.csv(file = "District_Overall_Shares_03.08.23.csv")

## Note: could also read in directly from the web:
# datahub <- read.csv(file = "https://assets.ctfassets.net/9fbw4onh0qc1/XfBEuMLMOBgHrhmjBdVpc/e9eef870c2c2cd14bb95996392944739/District_Overall_Shares_Oct15.csv")
# datahub <- read.csv(file = "https://assets.ctfassets.net/9fbw4onh0qc1/XfBEuMLMOBgHrhmjBdVpc/8e555b362876da16ba52c85be5b2effe/District_Overall_Shares_03.08.23.csv")

# inspect data files -----

## SEDA -----

# figure out what the variables are, what each row represents, etc.

View(seda)

## Data Hub -----

View(datahub)

# Prepare files for merge -----

## SEDA -----

# In the seda file, each row is district-subject-subgroup
# For now, just want to keep the subgroup==all rows

table(seda$subgroup)
nrow(seda) # original rows
seda <- filter(seda, subgroup=="all")
nrow(seda) # how many rows are left?

# how many unique districts?
length(unique(seda$sedaadmin))

# what variables?
sumtable(seda)
names(seda)

# for now, I only want to keep:
# stateabb, sedaadmin, sedaaminname, subject, subgroup, gys_chg_ol
# gys_chg_ol is the change in average test scores from 2019 to 2022

seda <- seda %>%
  select(stateabb, sedaadmin, sedaadminname, subject, subgroup,
         gys_chg_ol)

sumtable(seda)

## Datahub -----

# how many districts in the datahub file?

nrow(datahub)
length(unique(datahub$NCESDistrictID))

# Great, this file is already one row per district, although it has more 
# districts than SEDA file.

# Need to change the variable NCESDistrictID to sedaadmin to match seda

# Actually, I'll create a new variable called sedaadmin so that I have the original too

datahub <- datahub %>%
  mutate(sedaadmin=NCESDistrictID)

# Merge files -----

# Now I use left_join, which will use the first data frame and add on elements that match

?left_join

data_merge <- left_join(seda, datahub, by = "sedaadmin")

nrow(data_merge)
nrow(seda)

length(unique(data_merge$sedaadmin))
length(unique(seda$sedaadmin))

sumtable(data_merge)

# Handle missing data -----

# there are some districts that are missing the share_xxxxx variables
# these must not have appeared in the datahub data
# let's see which states they are from:

filter(data_merge, is.na(share_inperson)) %>%
  with(., table(stateabb))

# appear to mostly be from OK; perhaps OK reported data differently

# it would be worth following this up, but for now, we will drop those rows using filter()

nrow(data_merge)
data_merge_nomiss <- filter(data_merge, !is.na(share_inperson))
nrow(data_merge_nomiss)
length(unique(data_merge_nomiss$sedaadmin))

# in the paper you'd want to indicate the total number of districts in the original seda file:
length(unique(seda$sedaadmin))

# and then the number kept after merging and dropping districts with missing data
length(unique(data_merge_nomiss$sedaadmin))

# Label variables -----

# at this point we could adjust variable labels
var_label(data_merge_nomiss)

# these labels get used in tab_model() for example

# here is how you can change them:

var_label(seda$gys_chg_ol)
var_label(seda$gys_chg_ol) <- "Estimated change in scores 2019-2022"
var_label(seda$gys_chg_ol)

var_label(data_merge_nomiss$share_inperson) <- "percent of year in person"

# Create GMC and group (state) mean centered variables #####

# I'll create a state mean centered version of share_inperson called share_inperson_cwc
# The "groups" are states, so this will represent share_inperson at each district, relative to state mean
# I will do the state mean centering separately by subject, because later on I
# will analyze the data separately by subjects
# I will also add state mean share_inperson as share_inperson_avg

data_merge_nomiss <- data_merge_nomiss %>%
  group_by(stateabb, subject) %>%
  mutate(
    share_inperson_cwc = share_inperson-mean(share_inperson),
    share_inperson_avg = mean(share_inperson)
  ) %>%
  ungroup() %>%
  group_by(subject) %>%
  mutate(
    share_inperson_gmc = share_inperson-mean(share_inperson)
  ) %>%
  ungroup()

# check variables
sumtable(data_merge_nomiss)

# save out cleaned data -----

saveRDS(data_merge_nomiss, file = "seda_datahub_clean.Rds")
