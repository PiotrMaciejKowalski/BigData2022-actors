def simple_metric(rankings: Dict[str, List[str], query_data: pd.DataFrame, reference_data: pd.DataFrame) ➝ float:
    result = 0
    suma = 0
    pozycja = 0
    for actor in rankings:
        for other_actor in rankings[actor]:
            licznik = 0
            if query_data['category']where(query_data['nconst'] = actor) = reference_data['category']where(reference_data['nconst'] = other_actor):
                licznik += 1
            sum += licznik/max_licznik * (len(lista_id_aktorow) - pozycja)
        
                                 
"""
rankings - odwzorowanie, które gromadzi stałe top n-rekomendacji. Same n może zostać wydedukowane z rozmiaru list, który musi być stały
query_data - dane ze zbioru testowanych aktorów, to nie muszą być te same kolumny, które biorą udział w trenowaniu. To są dane aktorów dla których wyznaczane są rekomendacje.
reference_data - dane ze zbioru referencyjnego. To dane aktorów, którzy mogli być zarekomendowani.
"""
