import pandas as pd
from scipy.stats import mannwhitneyu
import math


def read_file(file, sample_size=None):
    df = pd.read_csv(
    file, 
    sep=r"\[|\]\s=",
    index_col=False,
    skipinitialspace=True,
    names=['Variable', 'Project', 'Ratio'],
    engine='python',
    usecols=['Project', 'Ratio'],)
    df = df[df['Ratio'] != " NaN"]
    df['Ratio'] = pd.to_numeric(df['Ratio'])
    if(sample_size != None):
        df = df.sample(sample_size)
    return df


def main():
    # Aufgabe 2 a)
    sample_size = 100_000
    significance_niveau = 0.01

    python_try_statement_ratio_df = read_file('./python_ratio.txt', sample_size)
    java_try_statement_ratio_df = read_file('./java_ratio.txt', sample_size)

    python_try_statement_ratio_mean = python_try_statement_ratio_df['Ratio'].mean()
    python_try_statement_ratio_variance = python_try_statement_ratio_df['Ratio'].var()

    java_try_statement_ratio_mean = java_try_statement_ratio_df['Ratio'].mean()
    java_try_statement_ratio_variance = java_try_statement_ratio_df['Ratio'].var()

    cohens_d = abs(python_try_statement_ratio_mean - java_try_statement_ratio_mean) / \
                math.sqrt((python_try_statement_ratio_variance+java_try_statement_ratio_variance)/2)

    results = mannwhitneyu(java_try_statement_ratio_df['Ratio'], python_try_statement_ratio_df['Ratio'])

    print("Aufgabe 2 a)")
    print("Sample Size: " + sample_size)
    print('Python Try Statment Ratio Mean:' + str(python_try_statement_ratio_mean))
    print('Python Try Statment Ratio Variance:'+str(python_try_statement_ratio_variance))
    print('Java Try Statment Ratio Mean:' + str(java_try_statement_ratio_mean))
    print('Java Try Statment Ratio Variance:' + str(java_try_statement_ratio_variance))
    print("Mann-Whitney U Test p-value: " + str(results.pvalue))
    print("Are the results significant? " + str(results.pvalue < 0.01))
    print("Cohend's d (Effektstärke): " + cohens_d)
    print()

    # Aufgabe 2 b)

    python_start = read_file('./python_ratio.txt', sample_size)
    java_start = read_file('./java_ratio.txt', sample_size)

    def mannwhitneyu_p(n):
        python_df = python_start.sample(n)
        java_df = java_start.sample(n)
        return mannwhitneyu(java_df['Ratio'], python_df['Ratio']).pvalue

    python_full = read_file('./python_ratio.txt', sample_size)
    java_full = read_file('./java_ratio.txt', sample_size)

    uppper_bound = 100_000
    lower_bound = 1
    test_per_iteration = 50

    counter = 0

    print("Aufgabe 2 b)")
    while True:
        current_sample_size = int((uppper_bound+lower_bound)/2)

        pvalues = list()
        for i in range(test_per_iteration):
            pvalues.append(mannwhitneyu_p(current_sample_size))
        p = sum(pvalues) / len(pvalues)
        
        print(f"#{counter}, upper_bound: {uppper_bound}, lower_bound={lower_bound}, size: {current_sample_size}, is_significant: {p < 0.01}")
        counter+=1

        if(abs(uppper_bound - lower_bound) <= 1):
            print(f"#{counter}, upper_bound: {uppper_bound}, lower_bound={lower_bound}, size: {current_sample_size}, is_significant: {p < 0.01}")
            break

        if(p < 0.01):
            uppper_bound = current_sample_size
        else:
            lower_bound = current_sample_size
    print()

    # Aufgabe 3)
    python_try_statement_ratio_df = read_file('./python_ratio.txt')
    java_try_statement_ratio_df = read_file('./java_ratio.txt')

    python_try_statement_ratio_mean = python_try_statement_ratio_df['Ratio'].mean()
    python_try_statement_ratio_variance = python_try_statement_ratio_df['Ratio'].var()

    java_try_statement_ratio_mean = java_try_statement_ratio_df['Ratio'].mean()
    java_try_statement_ratio_variance = java_try_statement_ratio_df['Ratio'].var()

    cohens_d = abs(python_try_statement_ratio_mean - java_try_statement_ratio_mean) / \
                math.sqrt((python_try_statement_ratio_variance+java_try_statement_ratio_variance)/2)

    print("Aufgabe 3")
    print(f"Cohend's d (Effektstärke) für alle Daten: {cohens_d}")

    ### HIER SOLLTE IHR PROGRAMMKODE FOLGEN !!!

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


