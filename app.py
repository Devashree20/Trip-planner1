# app.py
import streamlit as st
from datetime import datetime
from backend import fetch_flights, extract_cheapest_flights, format_datetime, generate_itinerary

st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# --- Title Section ---
st.markdown("<h1 style='text-align:center;color:#ff5733;'>✈️ AI-Powered Travel Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;'>Plan your dream trip with AI — flights, hotels & itinerary all in one place.</p>", unsafe_allow_html=True)

# --- User Inputs ---
col1, col2 = st.columns(2)
with col1:
    source = st.text_input("🛫 Departure City (IATA Code):", "BOM")
    departure_date = st.date_input("📅 Departure Date")
with col2:
    destination = st.text_input("🛬 Destination (IATA Code):", "DEL")
    return_date = st.date_input("📅 Return Date")

num_days = st.slider("🕒 Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox("🎭 Travel Theme:", ["💑 Couple Getaway", "👨‍👩‍👧‍👦 Family Vacation", "🏔️ Adventure Trip", "🧳 Solo Exploration"])
activity_preferences = st.text_area("🎯 Favorite Activities:", "Relaxing on the beach, exploring historical sites")
budget = st.radio("💰 Budget Preference:", ["Economy", "Standard", "Luxury"])

st.markdown("---")

if st.button("🚀 Generate Travel Plan"):
    # Step 1: Fetch flights
    with st.spinner("✈️ Fetching flight data..."):
        flight_data = fetch_flights(source, destination, departure_date, return_date)
        cheapest_flights = extract_cheapest_flights(flight_data)

    st.subheader("🛫 Cheapest Flights")
    if cheapest_flights:
        cols = st.columns(len(cheapest_flights))
        for idx, flight in enumerate(cheapest_flights):
            with cols[idx]:
                airline_name = flight.get("airline", "Unknown Airline")
                price = flight.get("price", "N/A")
                st.markdown(f"**{airline_name}** — 💰 {price}")
    else:
        st.warning("No flight data available.")

    # Step 2: Generate itinerary
    with st.spinner("🗺️ Creating your personalized itinerary..."):
        itinerary = generate_itinerary(destination, num_days, travel_theme, activity_preferences, budget)

    st.success("✅ Travel Plan Generated Successfully!")
    st.subheader("🗓️ Your AI-Powered Itinerary:")
    st.write(itinerary)
