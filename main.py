import finnhub
from datetime import datetime, timedelta
import time

# הגדרת הלקוח עם מפתח ה-API
finnhub_client = finnhub.Client(api_key="ctqjlopr01qpe8vallu0ctqjlopr01qpe8vallug")

def get_stock_price(symbol: str):
    """קבלת מחיר מניה עדכני"""
    try:
        quote = finnhub_client.quote(symbol)
        print(f"\nמידע על מניית {symbol}:")
        print(f"מחיר נוכחי: ${quote['c']}")
        print(f"שינוי: ${quote['d']}")
        print(f"אחוז שינוי: {quote['dp']}%")
        print(f"מחיר פתיחה: ${quote['o']}")
        print(f"מחיר גבוה: ${quote['h']}")
        print(f"מחיר נמוך: ${quote['l']}")
        return quote
    except Exception as e:
        print(f"שגיאה בקבלת מידע על {symbol}: {str(e)}")
        return None

def get_company_profile(symbol: str):
    """קבלת מידע פיננסי בסיסי על חברה"""
    try:
        profile = finnhub_client.company_profile2(symbol=symbol)
        print(f"\nפרופיל חברה - {symbol}:")
        print(f"שם: {profile.get('name', 'לא זמין')}")
        print(f"מדינה: {profile.get('country', 'לא זמין')}")
        print(f"ענף: {profile.get('finnhubIndustry', 'לא זמין')}")
        print(f"מטבע: {profile.get('currency', 'לא זמין')}")
        print(f"שווי שוק: ${profile.get('marketCapitalization', 'לא זמין')}M")
        print(f"מספר עובדים: {profile.get('employeeTotal', 'לא זמין')}")
        print(f"אתר: {profile.get('weburl', 'לא זמין')}")
        return profile
    except Exception as e:
        print(f"שגיאה בקבלת פרופיל חברה {symbol}: {str(e)}")
        return None

def get_company_news(symbol: str):
    """קבלת חדשות על החברה"""
    try:
        # קבלת חדשות מהחודש האחרון
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        news = finnhub_client.company_news(symbol, start_date, end_date)
        
        print(f"\nחדשות אחרונות על {symbol}:")
        for article in news[:5]:  # מציג 5 חדשות אחרונות
            print(f"כותרת: {article.get('headline', 'לא זמין')}")
            print(f"תאריך: {datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d')}")
            print(f"סיכום: {article.get('summary', 'לא זמין')}")
            print(f"מקור: {article.get('source', 'לא זמין')}")
            print("---")
    except Exception as e:
        print(f"שגיאה בקבלת חדשות על {symbol}: {str(e)}")

def get_company_peers(symbol: str):
    """קבלת רשימת חברות דומות"""
    try:
        peers = finnhub_client.company_peers(symbol)
        print(f"\nחברות דומות ל-{symbol}:")
        for peer in peers:
            print(f"- {peer}")
        return peers
    except Exception as e:
        print(f"שגיאה בקבלת חברות דומות ל-{symbol}: {str(e)}")
        return []

def get_recommendation_trends(symbol: str):
    """קבלת המלצות אנליסטים"""
    try:
        trends = finnhub_client.recommendation_trends(symbol)
        if trends:
            latest = trends[0]  # מידע אחרון
            print(f"\nהמלצות אנליסטים ל-{symbol}:")
            print(f"תאריך: {latest.get('period', 'לא זמין')}")
            print(f"קניה חזקה: {latest.get('strongBuy', 0)}")
            print(f"קניה: {latest.get('buy', 0)}")
            print(f"החזק: {latest.get('hold', 0)}")
            print(f"מכירה: {latest.get('sell', 0)}")
            print(f"מכירה חזקה: {latest.get('strongSell', 0)}")
    except Exception as e:
        print(f"שגיאה בקבלת המלצות אנליסטים ל-{symbol}: {str(e)}")

def get_company_earnings(symbol: str):
    """קבלת נתוני רווחים"""
    try:
        earnings = finnhub_client.company_earnings(symbol)
        print(f"\nנתוני רווחים ל-{symbol}:")
        for quarter in earnings[:4]:  # 4 רבעונים אחרונים
            print(f"רבעון: {quarter.get('period', 'לא זמין')}")
            print(f"רווח צפוי: ${quarter.get('estimate', 'לא זמין')}")
            print(f"רווח בפועל: ${quarter.get('actual', 'לא זמין')}")
            print("---")
    except Exception as e:
        print(f"שגיאה בקבלת נתוני רווחים ל-{symbol}: {str(e)}")

def get_company_financials(symbol: str):
    """קבלת נתונים פיננסיים בסיסיים"""
    try:
        metrics = finnhub_client.company_basic_financials(symbol, 'all')
        if 'metric' in metrics:
            print(f"\nנתונים פיננסיים ל-{symbol}:")
            metrics = metrics['metric']
            print(f"P/E: {metrics.get('peBasicExclExtraTTM', 'לא זמין')}")
            print(f"ROE: {metrics.get('roeTTM', 'לא זמין')}%")
            print(f"מרווח רווח: {metrics.get('grossMarginTTM', 'לא זמין')}%")
            print(f"צמיחת הכנסות: {metrics.get('revenueGrowthTTM3Y', 'לא זמין')}%")
            print(f"יחס חוב להון: {metrics.get('totalDebt/totalEquityQuarterly', 'לא זמין')}")
    except Exception as e:
        print(f"שגיאה בקבלת נתונים פיננסיים ל-{symbol}: {str(e)}")

def get_insider_transactions(symbol: str):
    """קבלת מידע על עסקאות של אנשי פנים"""
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        transactions = finnhub_client.stock_insider_transactions(symbol, start_date, end_date)
        
        print(f"\nעסקאות אנשי פנים ב-{symbol}:")
        for trans in transactions.get('data', [])[:5]:  # 5 עסקאות אחרונות
            print(f"שם: {trans.get('name', 'לא זמין')}")
            print(f"תפקיד: {trans.get('transactionCode', 'לא זמין')}")
            print(f"כמות: {trans.get('share', 'לא זמין')}")
            print(f"מחיר: ${trans.get('price', 'לא זמין')}")
            print(f"תאריך: {trans.get('filingDate', 'לא זמין')}")
            print("---")
    except Exception as e:
        print(f"שגיאה בקבלת עסקאות אנשי פנים ל-{symbol}: {str(e)}")

if __name__ == "__main__":
    symbol = 'CMCT'
    print(f"\n=== מידע מורחב על מניית {symbol} ===")
    
    # מידע בסיסי
    get_stock_price(symbol)
    get_company_profile(symbol)
    
    # חתונים פיננסיים
    get_company_financials(symbol)
    get_company_earnings(symbol)
    
    # עסקאות אנשי פנים
    get_insider_transactions(symbol)
    
    # חדשות והמלצות
    get_company_news(symbol)
    get_recommendation_trends(symbol)
    
    # חברות דומות
    get_company_peers(symbol)
