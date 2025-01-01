import streamlit as st
import finnhub
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go

# הגדרת הלקוח עם מפתח ה-API
finnhub_client = finnhub.Client(api_key="ctqjlopr01qpe8vallu0ctqjlopr01qpe8vallug")

def get_stock_price(symbol: str):
    """קבלת מחיר מניה עדכני"""
    try:
        return finnhub_client.quote(symbol)
    except Exception as e:
        st.error(f"שגיאה בקבלת מחיר המניה: {str(e)}")
        return None

def get_company_profile(symbol: str):
    """קבלת מידע פיננסי בסיסי על חברה"""
    try:
        return finnhub_client.company_profile2(symbol=symbol)
    except Exception as e:
        st.error(f"שגיאה בקבלת פרופיל החברה: {str(e)}")
        return None

def get_company_news(symbol: str):
    """קבלת חדשות על החברה"""
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        return finnhub_client.company_news(symbol, start_date, end_date)
    except Exception as e:
        st.error(f"שגיאה בקבלת חדשות: {str(e)}")
        return []

def get_company_financials(symbol: str):
    """קבלת נתונים פיננסיים"""
    try:
        return finnhub_client.company_basic_financials(symbol, 'all')
    except Exception as e:
        st.error(f"שגיאה בקבלת נתונים פיננסיים: {str(e)}")
        return None

def get_recommendation_trends(symbol: str):
    """קבלת המלצות אנליסטים"""
    try:
        return finnhub_client.recommendation_trends(symbol)
    except Exception as e:
        st.error(f"שגיאה בקבלת המלצות: {str(e)}")
        return []

def main():
    st.set_page_config(page_title="מעקב מניות", layout="wide", initial_sidebar_state="expanded")
    
    # כותרת ראשית
    st.title("🚀 דשבורד מעקב מניות")
    
    # תיבת טקסט להזנת סימבול
    symbol = st.text_input("הכנס סימבול מניה (לדוגמה: AAPL)").upper()
    
    if symbol:
        # יצירת 3 עמודות
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # מידע על מחיר המניה
        quote = get_stock_price(symbol)
        if quote:
            with col1:
                st.subheader("📈 מחיר המניה")
                price_delta = quote['c'] - quote['pc']
                price_delta_percent = (price_delta / quote['pc']) * 100
                
                st.metric(
                    label="מחיר נוכחי",
                    value=f"${quote['c']:.2f}",
                    delta=f"{price_delta:.2f}$ ({price_delta_percent:.2f}%)"
                )
                
                st.write(f"מחיר פתיחה: ${quote['o']:.2f}")
                st.write(f"מחיר גבוה: ${quote['h']:.2f}")
                st.write(f"מחיר נמוך: ${quote['l']:.2f}")
        
        # מידע על החברה
        profile = get_company_profile(symbol)
        if profile:
            with col2:
                st.subheader("ℹ️ פרופיל החברה")
                st.write(f"**שם:** {profile.get('name', 'לא זמין')}")
                st.write(f"**ענף:** {profile.get('finnhubIndustry', 'לא זמין')}")
                st.write(f"**מדינה:** {profile.get('country', 'לא זמין')}")
                st.write(f"**שווי שוק:** ${profile.get('marketCapitalization', 0):.2f}M")
        
        # נתונים פיננסיים
        financials = get_company_financials(symbol)
        if financials and 'metric' in financials:
            with col3:
                st.subheader("💰 נתונים פיננסיים")
                metrics = financials['metric']
                st.write(f"**P/E:** {metrics.get('peBasicExclExtraTTM', 'לא זמין')}")
                st.write(f"**ROE:** {metrics.get('roeTTM', 'לא זמין')}%")
                st.write(f"**מרווח רווח:** {metrics.get('grossMarginTTM', 'לא זמין')}%")
                st.write(f"**יחס חוב להון:** {metrics.get('totalDebt/totalEquityQuarterly', 'לא זמין')}")
        
        # המלצות אנליסטים
        trends = get_recommendation_trends(symbol)
        if trends:
            st.subheader("👥 המלצות אנליסטים")
            latest = trends[0]
            
            # יצירת תרשים המלצות
            fig = go.Figure(data=[
                go.Bar(name='מספר אנליסטים', 
                      x=['קניה חזקה', 'קניה', 'החזק', 'מכירה', 'מכירה חזקה'],
                      y=[latest.get('strongBuy', 0), 
                         latest.get('buy', 0),
                         latest.get('hold', 0),
                         latest.get('sell', 0),
                         latest.get('strongSell', 0)],
                      text=[latest.get('strongBuy', 0),
                            latest.get('buy', 0),
                            latest.get('hold', 0),
                            latest.get('sell', 0),
                            latest.get('strongSell', 0)],
                      textposition='auto')
            ])
            
            fig.update_layout(title=f"המלצות אנליסטים - {latest.get('period', '')}")
            st.plotly_chart(fig, use_container_width=True)
        
        # חדשות
        news = get_company_news(symbol)
        if news:
            st.subheader("📰 חדשות אחרונות")
            for article in news[:5]:
                with st.expander(article.get('headline', 'ללא כותרת')):
                    st.write(f"**תאריך:** {datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d')}")
                    st.write(f"**מקור:** {article.get('source', 'לא זמין')}")
                    st.write(f"**סיכום:** {article.get('summary', 'לא זמין')}")

if __name__ == "__main__":
    main() 