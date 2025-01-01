# דשבורד מעקב מניות

דשבורד אינטראקטיבי למעקב אחר מניות בזמן אמת באמצעות Finnhub API.

## תכונות
- מעקב אחר מחירי מניות בזמן אמת
- מידע על פרופיל החברה
- נתונים פיננסיים
- המלצות אנליסטים
- חדשות אחרונות

## התקנה

1. התקן את החבילות הנדרשות:
```bash
pip install -r requirements.txt
```

2. הרץ את האפליקציה:
```bash
streamlit run dashboard.py
```

## שימוש
1. הזן סימבול מניה (למשל: AAPL, MSFT, GOOGL)
2. צפה במידע בזמן אמת
3. עקוב אחר המלצות והחדשות

## טכנולוגיות
- Python
- Streamlit
- Finnhub API
- Plotly 