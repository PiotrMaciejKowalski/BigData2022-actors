def simple_metric(rankings: Dict[str, List[str], query_data: pd.DataFrame, reference_data: pd.DataFrame) ➝ float:
    result = 0
    suma = 0
    pozycja = 0
    for actor in rankings:
        for other_actor in rankings[actor]:
            licznik = 0
            if query_data.loc[query_data['nconst'] == actor, 'category'].iloc[0] ==  reference_data.loc[ reference_data['nconst'] == other_actor, 'category'].iloc[0]
               licznik += 1
            if query_data.loc[query_data['nconst'] == actor, 'top_titleType'].iloc[0] ==  reference_data.loc[ reference_data['nconst'] == other_actor, 'top_titleType'].iloc[0]
                licznik += 1
            if query_data.loc[query_data['nconst'] == actor, 'top_genres'].iloc[0] ==  reference_data.loc[ reference_data['nconst'] == other_actor, 'top_genres'].iloc[0]
                licznik += 1
            if set(query_data.loc[query_data['nconst'] == actor, 'characters']) & set(reference_data.loc[ reference_data['nconst'] == other_actor, 'category']) != set()
               licznik += 1    
            if set(query_data.loc[query_data['nconst'] == actor, 'originalTitle']) & set(reference_data.loc[ reference_data['nconst'] == other_actor, 'originalTitle']) != set()
               licznik += 1   
            sum += licznik/5 * (5 - pozycja) #d dla pięciu aktorów oraz 5 parametrów
        result = sum/120
    return resul
                                 
"""
rankings - odwzorowanie, które gromadzi stałe top n-rekomendacji. Same n może zostać wydedukowane z rozmiaru list, który musi być stały
query_data - dane ze zbioru testowanych aktorów, to nie muszą być te same kolumny, które biorą udział w trenowaniu. To są dane aktorów dla których wyznaczane są rekomendacje.
reference_data - dane ze zbioru referencyjnego. To dane aktorów, którzy mogli być zarekomendowani.
"""
