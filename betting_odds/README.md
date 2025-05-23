# NBA Player Props Hub - Matchup-Centric Value Overview

This module provides a matchup-centric view of NBA player prop odds, with a focus on identifying potential value betting opportunities.

## Features

- **Matchup-First Approach**: Select a game to view all participating players and their props
- **Value Indicators**: Compare prop lines against player averages to identify potential betting opportunities
- **Multiple Stat Projections**: Choose between Last 5, Last 10, Season Average, or Season Median as your baseline
- **Sportsbook Selection**: Filter odds by sportsbook
- **Prop Category Focus**: Focus on specific prop types (Points, Rebounds, Assists)

## Architecture

The module consists of:

- **Models**: Data structures for matchups, player stats, and value indicators
- **Services**: Business logic for fetching and processing matchup data
- **UI**: Components for rendering player prop tables and other UI elements
- **Main Page**: The Streamlit page that ties everything together

## Current Limitations

This MVP uses mock data for:
- Available matchups for a given date
- Player statistics
- Some player prop data (if not available in the database)

In a future version, these will be replaced with real data from NBA APIs and your odds database.

## Running the Application

The application is integrated into the main Streamlit app and can be accessed via the "Betting Odds" page in the navigation.

To run the application:

```bash
streamlit run app.py
```

Then navigate to the "Betting Odds" page from the menu.

## Future Enhancements

Planned enhancements for future versions:

1. Real-time data integration with NBA API for player stats
2. Historical performance analysis against the line
3. Advanced value calculation with true probability estimation
4. Trend indicators for player performance
5. Team defense adjustments for more accurate projections 