import pytest
from src.modeling import ForurensningsLokasjon
print(hei)
def test_forurensnings_lokasjon_valid_data():
    """Tester at modellen godtar korrekte data"""
    # 1. ARRANGE (Klargjør testdata)
    test_input = {
        "name": "Oslo",
        "longitude": 10.75,
        "latitude": 59.91  # Her bruker vi det vi ØNSKER skal være riktig
    }
    
    # 2. ACT (Utfør handlingen)
    lokasjon = ForurensningsLokasjon(**test_input)
    
    # 3. ASSERT (Sjekk at resultatet er som forventet)
    assert lokasjon.name == "Oslo"
    assert lokasjon.latitude == 59.91 # Denne vil feile hvis du har skrevet 'latutude' i modellen!
    print(hei)