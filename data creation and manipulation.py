# custom function to call eps estimate data from an API, clean and manipulate the dataframe for future process steps
# requires subscription to Quandl
# inputs required are list of ticker symbols, start and end date
# future upgrade to code, update to perform asynchronous API calls

def get_eps_estimates(tickers, start_date, end_date):
    print('now pulling estimates...')
    quandl_text = open(r'\keys\quandl key.txt','r')
    quandl_key = quandl_text.read()
    quandl_text.close()
    quandl.ApiConfig.api_key = quandl_key
    df_append = []
    df_est = pd.DataFrame([])
    for tic in tickers:
        print(tic)
        time.sleep(1)
        try:
            data = quandl.get_table('ZACKS/EEH', qopts={'columns':['m_ticker', 'ticker', 'comp_name', 'per_end_date', 'per_fisc_qtr', 'per_fisc_year', 'per_cal_qtr', 'per_cal_year', 'obs_date', 'eps_mean_est']}, ticker= '{}'.format(tic), per_type = 'Q', per_end_date = {'gte': start_date})
            df_append = pd.DataFrame(data)
        
            # In the idx = line below, by using end_date instead of max obs_date to find each company's last estimate date, it fills in deltas to the present day. 
            # This is making the assumption that the company continues to exist and carries forward the last estimates produced to the present day. 
            # Deltas will eventually null this out to zero if the last estimates produced were more than the delta_days ago. 
            # Potential fix is find the difference between end_date and the last observation date. If greater than x, then stop at that date, else carry forward to end_date.
            # df_append['obs_date'].max() <-- this can replace end_date in the line below.
            idx = pd.date_range(df_append['obs_date'].min(), end_date)

            # Interpolate missing dates carrying forward last known get_eps_estimate
            df_append = df_append.groupby(['ticker', 'per_end_date', 'per_fisc_qtr', 'per_fisc_year', 'per_cal_qtr', 'per_cal_year']).apply(lambda x: x.set_index('obs_date').reindex(idx).fillna(method='ffill'))['eps_mean_est'].reset_index(level=1)
            df_append.reset_index(level=df_append.index.names, inplace=True)
            df_append['obs_date'] = df_append['level_5']
            df_append.drop(['level_5'], axis=1, inplace=True)

            # keep estimates less than 2 years old
            df_append = df_append[df_append['obs_date'] <= df_append['per_end_date']]
            df_append['days_fwd'] = (df_append['per_end_date'] - df_append['obs_date']).dt.days
            df_append = df_append[df_append['days_fwd'] <= 730]
            df_append['month'] = df_append['per_end_date'].dt.month
            df_append['year'] = df_append['per_end_date'].dt.year

            # standardize fiscal quarters
            df_append.loc[df_append['month'] < 2, 'std_year'] = df_append['year'] - 1
            df_append.loc[df_append['month'] >= 2, 'std_year'] = df_append['year']
            df_append['std_year'] = df_append['std_year'].astype(int)
            conditions = [
            (df_append['month'].isin([1, 11, 12])),
            (df_append['month'].isin([2, 3, 4])),
            (df_append['month'].isin([5, 6, 7])),
            (df_append['month'].isin([8, 9, 10]))
            ]
            choices = ['Q4', 'Q1', 'Q2', 'Q3']
            df_append['std_period'] = df_append['std_year'].map(str) + np.select(conditions, choices, default='MISSING')
            df_append = df_append.drop(['std_year', 'month', 'year'], axis=1)
            df_est = df_est.append(df_append)
        except ValueError:
            # add message for ticker causing error
            pass
    df_est.sort_values(['ticker', 'per_end_date', 'obs_date'], inplace=True)
    # df_est.to_pickle(r'E:\Earnings Alchemy\Data\estimates\est_' + str(save_date) + '.pkl')
    return df_est