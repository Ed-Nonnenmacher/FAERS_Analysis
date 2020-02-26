# FAERS_Analysis
# This is entirely for review purposes, and would like to apologize to any poor soul that attempts to fully follow main thread from file 0 - 3.  It works.  It will take time to read through the slop, but please understand I was given only 2 days to develop:

  ##   First: a re-usable system for parsing FAERS ASCII downloads
  ##   Second: A re-usable system for transforming FAERS drug exposure and outcomes into defined N by M adverse event frequency matrices.
  
# It's been butchered due to dozens of reanalysis and time constraints as this was a preliminary analysis to put in for a large grant to evaluate adverse events through exposures to SSRI, SNRI, and other drugs within other similar classes.



This is the first round of dis-proportionality screening and small chunks of adverse event frequency matrix and Fischer's Exact testing for significance.

FAERS_data_extract_0:  Compiles/concats FAERS quarters and years from base ASCII files into readable pandas dataframes.
FAERS_grouping_AE_1: Reformats and reclassifies diseases as more broad categories.  Needed for data cleaning.
Drug_output_2.v.1 (deprecated):  Original file for first combining product active ingredient with drugname.  Further data cleaning.Output are dependent variable file to be used for mining algorithms.
Drug_output_2.v.2:Simial to v.1 , but cut out prod_ai and drugname marriage, as this step is moved further down the pipeline for optimization purposes.
TableA_B_3: primary analytical file.  Has been cut down to only disproportionality analysis.  
