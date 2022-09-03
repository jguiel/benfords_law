import json
import plotly
import pandas as pd
import scipy.stats as stats
import plotly.express as px

ALLOWED_EXTENSIONS = {'txt', 'tsv', 'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def chisquare_plot(init_data):
    
    pd.options.plotting.backend = "plotly"
    benford_expected_map = [.301,.176,.125,.097,.079,.067,.058,.051,.046]                   # Benford expected frequencies

    benford_data = init_data.apply(                                                         # Isolates user-specified column
        lambda x: pd.Series(                                                                # Lambda function to transform values
            str(x[0]).split('.')[-1].lstrip('0')[0] if str(x[0]).split('.')[0] == '0'       # Extracts leading digit (excluding zeroes)
            else str(x[0]).split('.')[0][0]                                                 # Splits at decimal to try and find leading digit
            ), axis=1                                                                       # Chooses first digit if > 1, and first 
        )                                                                                   # non-zero decimal if < 1
    
    benford_observed = benford_data.value_counts().sort_index().reset_index(drop=True)      # Non-normalized counts of each leading digit
    benford_observed_freq = benford_data.value_counts(normalize=True).sort_index()          # Normalized frequencies of eeach leading digit
    
    n = benford_observed.sum()
    benford_expected_freq = pd.Series(benford_expected_map)                                 # Pandas series object of frequencies
    benford_expected = pd.Series([freq * n for freq in benford_expected_map])               # Theoretical counts of expected values
                                                                                            # Generated using frequency * number obs. values
    try:
        test_statistic, p_value = stats.chisquare(
            f_obs=benford_observed,
            f_exp=benford_expected
            )
        benford_fit = True if p_value > 0.05 else False
        
    except Exception as e:
        test_statistic, p_value, benford_fit = False, False, False 

    leading_digits = [n+1 for n in range(9)]
    
    figure = px.line(                           # Initial line graph
        x=leading_digits,                       # Expected frequencies
        y=benford_expected_freq,
        color=px.Constant("Expected Frequencies"),
        labels=dict(x='Leading Digit',y='Frequency in Dataset')
        )
    
    figure.add_bar(                             # Overlay bar graph
        x=leading_digits,                       # Observed frequencies
        y=benford_observed_freq,
        name='Observed Frequencies'
        )
    
    figure.add_annotation(                      # Add annotations from Chi2
        text=f'p = {round(p_value,4)}',         # p-value and test statistic on graph
        name="p-value",                                  
        xref="paper", yref="paper",
        x=0.25, y=0.90, showarrow=False,
        font=dict(size=12, color="black")
        )
    
    figure.add_annotation(text=f'Test Statistic = {round(test_statistic,2)}',
        name="Test Statistic",                                  
        xref="paper", yref="paper",
        x=0.75, y=0.90, showarrow=False,
        font=dict(size=12, color="black")
        )
    
    graph_json = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json, benford_fit, test_statistic, p_value