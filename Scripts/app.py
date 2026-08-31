import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

from pathlib import Path

# Hotfix for Plotly/Pandas compatibility
pd.DataFrame.iteritems = pd.DataFrame.items

# ==========================================
# 1. LOAD AND CLEAN DATA 
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Datasets" / "coffee_renamed.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found at expected path: {DATA_PATH}")

coffee_survey = pd.read_csv(DATA_PATH)

# Apply the categorical sorting so the charts look right
age_order = ['<18 years old', '18-24 years old', '25-34 years old', '35-44 years old', '45-54 years old', '55-64 years old', '>65 years old']
spend_order = ['<$20', '$20-$40', '$40-$60', '$60-$80', '$80-$100', '>$100']
cups_order = ['Less than 1', '1', '2', '3', '4', 'More than 4']

coffee_survey['age'] = pd.Categorical(coffee_survey['age'], categories=age_order, ordered=True)
coffee_survey['total_spend'] = pd.Categorical(coffee_survey['total_spend'], categories=spend_order, ordered=True)
coffee_survey['cups'] = pd.Categorical(coffee_survey['cups'], categories=cups_order, ordered=True)
coffee_survey['expertise'] = pd.to_numeric(coffee_survey['expertise'], errors='coerce')

# Extract only the primary (first) option from multiple-choice questions
# We split by comma (standard for Google Forms) or slash, grab the first item, and remove extra spaces
coffee_survey['brew'] = coffee_survey['brew'].str.split(r'[,/]').str[0].str.strip()
coffee_survey['purchase'] = coffee_survey['purchase'].str.split(r'[,/]').str[0].str.strip()


# ==========================================
# 2. CREATE THE PLOTLY FIGURES (Your Code!)
# ==========================================
age_counts = coffee_survey['age'].value_counts(sort=False).reset_index()
age_counts.columns = ['Age Group', 'Number of Participants']
fig_age = px.bar(age_counts, x='Age Group', y='Number of Participants', title="Age Distribution", color_discrete_sequence=['#636EFA'])

spend_counts = coffee_survey['total_spend'].value_counts(sort=False).reset_index()
spend_counts.columns = ['Monthly Spend', 'Number of Participants']
fig_spend = px.bar(spend_counts, x='Monthly Spend', y='Number of Participants', title="Monthly Spend", color_discrete_sequence=['#EF553B'])

cups_counts = coffee_survey['cups'].value_counts(sort=False).reset_index()
cups_counts.columns = ['Cups Per Day', 'Number of Participants']
fig_cups = px.bar(cups_counts, x='Cups Per Day', y='Number of Participants', title="Daily Consumption", color_discrete_sequence=['#00CC96'])

fig_expertise = px.histogram(coffee_survey, x='expertise', title="Coffee Expertise (1-10)", nbins=10, color_discrete_sequence=['#AB63FA'])
fig_expertise.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

# --- 5. Favorite Brew Method Plot ---
brew_counts = coffee_survey['brew'].value_counts().reset_index()
brew_counts.columns = ['Brewing Method', 'Count']

fig_brew = px.bar(
    brew_counts, 
    x='Count', 
    y='Brewing Method', 
    orientation='h', # Horizontal bar chart for long text labels
    title="How are they brewing at home?",
    color_discrete_sequence=['#FFA15A']
)
fig_brew.update_layout(yaxis={'categoryorder':'total ascending'}) # Sort longest bar to top


# --- 6. On-The-Go Purchase Plot ---
purchase_counts = coffee_survey['purchase'].value_counts().reset_index()
purchase_counts.columns = ['Purchase Location', 'Count']

fig_purchase = px.bar(
    purchase_counts, 
    x='Count', 
    y='Purchase Location', 
    orientation='h',
    title="Where do they buy coffee on the go?",
    color_discrete_sequence=['#19D3F3']
)
fig_purchase.update_layout(yaxis={'categoryorder':'total ascending'})


# --- 7. Taste Test Preference Plot ---
# Using the 'prefer_overall' column (which was their favorite of the 4 blind coffees)
taste_counts = coffee_survey['prefer_overall'].value_counts().reset_index()
taste_counts.columns = ['Favorite Coffee', 'Count']

fig_taste = px.pie(
    taste_counts, 
    names='Favorite Coffee', 
    values='Count', 
    title="Blind Taste Test: Which coffee won?",
    color_discrete_sequence=px.colors.sequential.Sunset
)


# --- 8. Willingness to Pay Plot ---
willing_counts = coffee_survey['most_willing'].value_counts().reset_index()
willing_counts.columns = ['Max Price Willing to Pay', 'Count']

# Let's organize the money logically rather than alphabetically
willing_order = ['Less than $2', '$2-$4', '$4-$6', '$6-$8', '$8-$10', '$10-$15', '$15-$20', 'More than $20']
coffee_survey['most_willing'] = pd.Categorical(coffee_survey['most_willing'], categories=willing_order, ordered=True)

willing_counts = coffee_survey['most_willing'].value_counts(sort=False).reset_index()
willing_counts.columns = ['Max Price Willing to Pay', 'Count']

fig_willing = px.bar(
    willing_counts, 
    x='Max Price Willing to Pay', 
    y='Count', 
    title="What's the most they would pay for a cup?",
    color_discrete_sequence=['#FF6692']
)


# ==========================================
# SLIDE 4 PLOTS: BUSTING THE MYTH (Bar Charts)
# ==========================================

# --- 1. Preferred Roast Level ---
roast_counts = coffee_survey['roast_level'].dropna().value_counts().reset_index()
roast_counts.columns = ['Roast Level', 'Number of Participants']

# A generous list from light to dark. Plotly will safely ignore any that aren't in your data.
roast_order = ['Nordic', 'Blonde', 'Light', 'Medium', 'Dark', 'French', 'Italian', 'Italian (Very Dark)']

fig_roast = px.bar(
    roast_counts, 
    x='Roast Level', 
    y='Number of Participants', 
    title="The Reality: Preferred Roast Levels",
    color='Roast Level',
    category_orders={"Roast Level": roast_order}, # <-- FIX: Let Plotly handle the sorting safely
    color_discrete_sequence=px.colors.sequential.Brwnyl)

# Hide the redundant legend
fig_roast.update_layout(showlegend=False)


# --- 2. Willingness to Pay ---
# Lock in the logical price order
willing_order = ['Less than $2', '$2-$4', '$4-$6', '$6-$8', '$8-$10', '$10-$15', '$15-$20', 'More than $20']
coffee_survey['most_willing'] = pd.Categorical(coffee_survey['most_willing'], categories=willing_order, ordered=True)

willing_counts = coffee_survey['most_willing'].dropna().value_counts(sort=False).reset_index()
willing_counts.columns = ['Max Price Willing to Pay', 'Number of Participants']

fig_willing = px.bar(
    willing_counts, 
    x='Max Price Willing to Pay', 
    y='Number of Participants', 
    title="What's the most they would pay for a cup?",
    color_discrete_sequence=['#FF6692']
)

# --- 3. Blind Taste Test Results (Coffees A, B, C, D) ---

# Grab the 4 preference columns
pref_cols = [
    'coffee_a_personal_preference', 'coffee_b_personal_preference',
    'coffee_c_personal_preference', 'coffee_d_personal_preference'
]

# Create a clean subset and rename the columns so your audience knows what the coffees actually were!
taste_df = coffee_survey[pref_cols].dropna().copy()
taste_df.columns = [
    'Coffee A (Light)', 'Coffee B (Medium)', 
    'Coffee C (Dark)', 'Coffee D (Light & Funky)'
]

# "Melt" the data from wide to long format (Plotly needs it this way for stacked bars)
taste_long = taste_df.melt(var_name='Coffee', value_name='Rating')

# Grab just the first character of the rating (e.g., turns "5.0" into "5") so we have clean categories
taste_long['Rating'] = taste_long['Rating'].astype(str).str[0]

# Count how many 1s, 2s, 3s, 4s, and 5s each coffee got
taste_counts = taste_long.groupby(['Coffee', 'Rating']).size().reset_index(name='Votes')

# Build the 100% Stacked Bar Chart
fig_taste_test = px.bar(
    taste_counts,
    x='Votes',
    y='Coffee',
    color='Rating',
    orientation='h',
    title="Blind Taste Test: How they rated the 4 mystery coffees",
    category_orders={
        "Rating": ["1", "2", "3", "4", "5"], # 1 = Hate it, 5 = Love it
        "Coffee": ['Coffee C (Dark)', 'Coffee B (Medium)', 'Coffee A (Light)', 'Coffee D (Light & Funky)']
    },
    # A custom Red-to-Green color scale
    color_discrete_sequence=['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#1a9850'] 
)

# Force the bars to stretch to 100% width for easy percentage comparisons
fig_taste_test.update_layout(
    barmode='stack', 
    barnorm='percent', 
    xaxis_title="Percentage of Tasters (%)"
)

# ==========================================
# SLIDE 5 PLOTS: EMPLOYMENT vs SPENDING BUBBLE CHART
# ==========================================

# 1. Grab the two columns and drop missing data
emp_df = coffee_survey[['employment_status', 'total_spend']].dropna().copy()

# 2. Keep only the Top 5 most common employment statuses to keep the chart looking clean
top_5_emp = emp_df['employment_status'].value_counts().head(5).index
emp_df = emp_df[emp_df['employment_status'].isin(top_5_emp)]

# 3. Group and count how many people fall into each specific combination
emp_counts = emp_df.groupby(['employment_status', 'total_spend']).size().reset_index(name='Count')

# 4. Generate the Bubble Chart
fig_emp = px.scatter(
    emp_counts,
    x='total_spend',
    y='employment_status',
    size='Count',          # The bubble gets bigger with more people
    color='Count',         # The bubble gets darker with more people
    color_continuous_scale=px.colors.sequential.Brwnyl, # Coffee themed colors
    size_max=45,           # Limits the maximum bubble size so they don't overlap
    title="Where the Money Is: Spending by Employment Status",
    labels={
        'total_spend': 'Monthly Coffee Budget',
        'employment_status': 'Employment Status'
    }
)

# --- 10. Dynamic Coffee Reasons Cross Matrix Plot (For Slide 1) ---

search_phrases = ['tastes good', 'caffeine', 'ritual', 'bathroom']
matrix_labels = ['Tastes Good', 'Caffeine', 'Ritual', 'To go to bathroom']

df_reasons = coffee_survey.dropna(subset=['why_drink']).copy()
total_respondents = len(df_reasons)

bool_df = pd.DataFrame()
for phrase, label in zip(search_phrases, matrix_labels):
    # FIX: Added .astype(int) at the end to force True=1 and False=0
    bool_df[label] = df_reasons['why_drink'].str.contains(phrase, case=False, na=False).astype(int)



# Calculate the co-occurrence matrix using explicit integers
co_matrix_counts = bool_df.T.dot(bool_df)

co_matrix_pct = (co_matrix_counts / total_respondents) * 100
co_matrix_pct = co_matrix_pct.round(0) 

fig_matrix = px.imshow(
    co_matrix_pct,
    labels=dict(x="", y="", color="Percentage"),
    x=matrix_labels,
    y=matrix_labels,
    color_continuous_scale='Reds',
    title="Why do you Drink Coffee?"
)

fig_matrix.update_traces(texttemplate="%{z}%", textfont_size=16)
fig_matrix.update_layout(
    coloraxis_showscale=False,
    xaxis=dict(side='top'),
    plot_bgcolor='white',
    margin=dict(t=80, b=20, l=20, r=20)
)


# ==========================================
# 3. BUILD THE DASH APP
# ==========================================
app = dash.Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}, children=[
    
    # The Main Presentation Title
    html.H1("The Great Dark Roast Delusion", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # The Tabs Container (Acts as your slide deck)
    dcc.Tabs(style={'fontWeight': 'bold'}, children=[
        
# ==========================================
        # SLIDE 1: EXPOSITION & THE HOFFMANN TEST
        # ==========================================
        dcc.Tab(label='1. The Hypothesis & Test', children=[
            html.Div(style={'padding': '40px', 'textAlign': 'center', 'marginTop': '20px'}, children=[
                html.H2("The Industry Assumption"),
                html.P(
                    "Welcome, fellow coffee shop owners. As we look to grow our online beans business, "
                    "we have to confront a massive assumption in our industry. The conventional wisdom is simple: "
                    "'People just want a standard, dark-roasted, bitter cup of black coffee. Keep it cheap, keep it simple.'",
                    style={'fontSize': '20px', 'maxWidth': '800px', 'margin': '0 auto', 'lineHeight': '1.6'}
                ),
                
                html.Br(),
                
                html.H2("The Great American Coffee Taste Test"),
                html.P(
                    "To see if that hypothesis holds up, we are analyzing 'The Great American Coffee Taste Test.' "
                    "Orchestrated by coffee expert James Hoffmann, this massive survey contained multiple questions related to coffee and sent four mystery coffees "
                    "to thousands of participants for a blind taste test. But before we look at the blind tasting results, "
                    "we need to understand their core motivation: why are they drinking coffee in the first place?",
                    style={'fontSize': '20px', 'maxWidth': '800px', 'margin': '0 auto', 'lineHeight': '1.6', 'marginBottom': '30px'}
                ),
                
                # The dynamic cross-matrix chart
                html.Div(dcc.Graph(figure=fig_matrix), style={'maxWidth': '600px', 'margin': '0 auto'}),
                
                # --- NEW ADDITION: The Data Citation ---
                html.Div(style={'marginTop': '30px', 'textAlign': 'center'}, children=[
                    html.Small([
                        "Data Source: ",
                        html.A(
                            "The Great American Coffee Taste Test (James Hoffmann)", 
                            href="https://www.kaggle.com/datasets/umerhaddii/the-great-american-coffee-taste-test-dataset", # <-- INSERT YOUR LINK HERE
                            target="_blank", # Opens link in a new tab
                            style={'color': '#EF553B', 'textDecoration': 'none'}
                        )
                    ], style={'color': 'gray', 'fontSize': '14px'})
                ])
                
            ])
        ]),

        # ==========================================
        # SLIDE 2: THE AUDIENCE
        # ==========================================
        dcc.Tab(label='2. Our Audience', children=[
            html.Div(style={'padding': '20px'}, children=[
                html.H2("Profile of the Flavor-Seeker", style={'textAlign': 'center'}),
                
                # Main narrative paragraph connecting Slide 1 to the demographics
                html.P(
                    "If they are drinking coffee for the taste and the ritual, who exactly are they? "
                    "By looking at the demographics of the Hoffmann Taste Test, we see that this isn't a casual consumer—this is a highly invested hobbyist.",
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '20px', 'maxWidth': '900px', 'margin': '0 auto 20px auto'}
                ),

                # Bullet points to make the 4 charts easy to digest quickly during a presentation
                html.Ul(style={'fontSize': '16px', 'maxWidth': '800px', 'margin': '0 auto 30px auto', 'lineHeight': '1.6'}, children=[
                    html.Li(html.B("Disposable Income: They are established adults consistently budgeting $40 to $80+ a month on beans.")),
                    html.Li(html.B("Quantity: They focus on 2 to 3 cups a day.")),
                    html.Li(html.B("Educated Palates: They rate their own expertise highly, meaning they know what they are tasting and won't settle for cheap beans."))
                ]),

                # 2x2 Grid for the audience plots
                html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}, children=[
                    html.Div(dcc.Graph(figure=fig_age), style={'width': '48%', 'padding': '10px'}),
                    html.Div(dcc.Graph(figure=fig_spend), style={'width': '48%', 'padding': '10px'}),
                    html.Div(dcc.Graph(figure=fig_cups), style={'width': '48%', 'padding': '10px'}),
                    html.Div(dcc.Graph(figure=fig_expertise), style={'width': '48%', 'padding': '10px'}),
                ])
            ])
        ]),

        # ==========================================
        # SLIDE 3: BREWING & BUYING HABITS
        # ==========================================
        dcc.Tab(label='3. Customer Habits', children=[
            html.Div(style={'padding': '20px'}, children=[
                html.H2("The Ritual in Practice: Brewing & Buying", style={'textAlign': 'center'}),
                
                # Narrative text connecting the demographics to their physical habits
                html.P(
                    "We have established that our target customers have the budget and the palate. "
                    "But how do they physically interact with coffee? The data shows these aren't consumers looking for convenience, rather they are looking for craft.",
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '20px', 'maxWidth': '900px', 'margin': '0 auto 20px auto'}
                ),

                # Scannable bullet points for your 10-minute presentation pace
                html.Ul(style={'fontSize': '16px', 'maxWidth': '800px', 'margin': '0 auto 30px auto', 'lineHeight': '1.6'}, children=[
                    
                    # FIX: Wrapped the html.B and the string in a list []
                    html.Li([
                        html.B("The Pour-Over Majority: "), 
                        "Manual brewing dominates. These customers are hands-on, meaning we must prioritize selling whole beans rather than pre-ground, mass-market bags."
                    ]),
                    
                    # FIX: Wrapped the html.B and the string in a list []
                    html.Li([
                        html.B("Seeking Specialty: "), 
                        "When they do buy coffee on the go, they opt for local specialty shops. They are already conditioned to pay a premium for better beans."
                    ])
                    
                ]), 

                # 2 Side-by-side plots
                html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
                    html.Div(dcc.Graph(figure=fig_brew), style={'width': '50%', 'padding': '10px'}),
                    html.Div(dcc.Graph(figure=fig_purchase), style={'width': '50%', 'padding': '10px'}),
                ])
            ])
        ]),

# ==========================================
        # SLIDE 4: THE CLIMAX (Busting the Myth)
        # ==========================================
        dcc.Tab(label='4. Busting the Myth', children=[
            html.Div(style={'padding': '20px'}, children=[
                html.H2("The Funky Sweet Spot & The Price Tag", style={'textAlign': 'center'}),
                
                # Narrative Text Part 1: The Mystery Coffees
                html.P(
                    "Here is where the conventional dark roast wisdom completely shatters. In a blind taste test of four mystery coffees, "
                    "the traditional dark roast (Coffee C) was rated the lowest. Conversely, the lighter, more complex roasts—specifically "
                    "Coffee A (a clean Light roast) and Coffee D (a Light & Funky profile)—took the top spots, with Coffee B (Medium) sitting safely in the middle.",
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '15px', 'maxWidth': '1000px', 'margin': '0 auto 15px auto'}
                ),
                
                # Narrative Text Part 2: The Business Value (Colored to stand out)
                html.P(
                    "But how does this translate to revenue? The data shows a strong willingness to pay $8 to $10 for a single premium cup at a cafe. "
                    "Since we are selling whole beans to home brewers, this works heavily in our favor. If a customer anchors the value of a great cup at $8, "
                    "selling them a $25 to $30 bag of specialty beans—which yields about 15 to 20 cups—positions our product as an incredibly high-value investment for their daily ritual.",
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '30px', 'maxWidth': '1000px', 'margin': '0 auto 30px auto', 'fontWeight': 'bold', 'color': '#EF553B'}
                ),
                
                # Top Row: The massive blind taste test result
                html.Div(dcc.Graph(figure=fig_taste_test), style={'width': '100%', 'padding': '10px'}),
                
                # Bottom Row: Self-reported roast preference and willingness to pay side-by-side
                html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
                    html.Div(dcc.Graph(figure=fig_roast), style={'width': '50%', 'padding': '10px'}),
                    html.Div(dcc.Graph(figure=fig_willing), style={'width': '50%', 'padding': '10px'}),
                ])
            ])
        ]),

# ==========================================
        # SLIDE 5: SUMMARY & STRATEGY
        # ==========================================
        dcc.Tab(label='5. Strategy & Summary', children=[
            html.Div(style={'padding': '20px', 'marginTop': '20px'}, children=[
                html.H2("The Final Verdict: Don't Compete on Price", style={'textAlign': 'center', 'marginBottom': '30px'}),
                
                # Split layout: Text on the left, Bubble Chart on the right
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}, children=[
                    
                    # Left Column: The Narrative
                    html.Div(style={'width': '35%', 'padding': '20px', 'textAlign': 'left'}, children=[
                        html.P(
                            "We started by questioning the industry assumption that people just want cheap, dark-roasted coffee. "
                            "The data tells a completely different story. Our audience is chasing flavor, mastering the pour-over ritual, and eagerly seeking out light, complex roasts.",
                            style={'fontSize': '18px', 'lineHeight': '1.6'}
                        ),
                        html.Br(),
                        html.P(
                            "Look at where the real money is concentrated on this chart. Our most lucrative segment consists of fully employed professionals who are allocating serious monthly budgets to fund their habit.",
                            style={'fontSize': '18px', 'lineHeight': '1.6'}
                        ),
                        html.Br(),
                        html.P(
                            "The Strategy: To maximize our online revenue, we must abandon the race to the bottom. We need to market premium, adventurous whole beans directly to these professionals as the ultimate upgrade for their daily home-office ritual.",
                            style={'fontSize': '19px', 'lineHeight': '1.6', 'fontWeight': 'bold', 'color': '#EF553B'}
                        )
                    ]),
                    
                    # Right Column: The Bubble Plot
                    html.Div(dcc.Graph(figure=fig_emp, style={'height': '600px'}), style={'width': '65%', 'padding': '10px'})
                ]) # Closes the split layout Div
            ]) # Closes the Slide 5 Div
        ]), # Closes Slide 5 dcc.Tab
        
        # ==========================================
        # SLIDE 6: THE CONCLUSION
        # ==========================================
        dcc.Tab(label='6. Conclusion', children=[
            html.Div(style={'padding': '20px', 'marginTop': '20px', 'textAlign': 'center'}, children=[
                html.H2("The Dark Roast Myth: Busted", style={'marginBottom': '20px'}),
                
                # The Final Narrative
                html.P(
                    "Our industry has operated on the assumption that convenience and dark roasts drive the market. "
                    "However, the data comprehensively proves otherwise.",
                    style={'fontSize': '20px', 'maxWidth': '900px', 'margin': '0 auto', 'lineHeight': '1.6'}
                ),
                html.Ul(style={'fontSize': '18px', 'maxWidth': '800px', 'margin': '20px auto 40px auto', 'textAlign': 'left', 'lineHeight': '1.8'}, children=[
                    html.Li([html.B("The Motivation: "), "They seek flavor and ritual, not just a caffeine jolt."]),
                    html.Li([html.B("The Method: "), "They are hands-on home brewers who rely on manual pour-overs."]),
                    html.Li([html.B("The Preference: "), "In blind tests, lighter, funkier roasts score higher than traditional dark roasts."]),
                    html.Li([html.B("The Opportunity: "), "They are fully employed professionals willing to pay a premium for craft."])
                ]),
                
                html.H3("The Data Story", style={'color': '#EF553B', 'marginBottom': '20px'}),
                
                # The Cycling Graph Container
                html.Div(dcc.Graph(id='cycling-graph'), style={'maxWidth': '900px', 'margin': '0 auto'}),
                
                # The Invisible Timer (Triggers every 4 seconds)
                dcc.Interval(
                    id='interval-component',
                    interval=4000, # 4000 milliseconds = 4 seconds
                    n_intervals=0
                )
            ])
        ]) # Closes Slide 6 dcc.Tab

    ]) # Closes dcc.Tabs (The slide deck)
]) # Closes the main app.layout html.Div


# ==========================================
# 4. DASH CALLBACKS (The Interactive Logic)
# ==========================================

@app.callback(
    Output('cycling-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # List of the key figures to loop through
    figs = [fig_matrix, fig_brew, fig_taste_test, fig_emp]
    
    # Use modulo to cycle through the list infinitely
    current_fig = figs[n % len(figs)]
    
    return current_fig


if __name__ == '__main__':
    # debug=True allows the app to update automatically if you change the code
    app.run(debug=True)