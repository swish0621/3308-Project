
# Web-Project
Team 4
Team Ralphie / Rage Ratio

- **Lucas Stackhouse**  
  GitHub: `lust6199`
- **Nicholas Swisher**  
  GitHub: `swish0621`
- **Nicole Sawtelle**  
  GitHub: `Nsawtelle`

---

## 🚀 How to Run This Project

### Prerequisites
- Firefox (front end must be run here)
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/)

### 1. Backend Setup (Flask)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd backend
# Create a .env file with your API keys and secrets (see .env.example if available)
python app.py
```
The backend will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 2. Frontend Setup (React)
#### Open a new shell
```bash
cd frontend/sentiment_app
npm install
npm start
```
The frontend will run on [http://localhost:3000](http://localhost:3000)

### 3. Usage
- Open the frontend URL in Firefox.
- Enter a game title to analyze sentiment and view live data.

---

## **Scheduled Meeting Time**
Sundays @ 6 pm MST

## **Project Overview & Planning**
### **Vision Statement** 
- To create a platform that empowers gamers to track live updates and game releases while analyzing public sentiment, offering real-time insights into how the gaming community reacts to new content.
### **Motivation**
- Updates to existing games have a major impact on the gaming community. The developers' choices in balancing gameplay, adding new content, or modifying base mechanics can trigger a wide range of reactions. These responses can be seen quickly across various online platforms, changing public perception and player engagement. By capturing and analyzing this sentiment in real time, we aim to better understand how updates influence community satisfaction.
### **Risks**
- The majority of our team has limited experience working on large-scale projects or collaborating in team environments.

- Communication may present challenges due to differing schedules, which could impact clear and timely sharing of updates and requirements.

- Several team members have little prior experience with AI tools or natural language processing models.

- Accurately interpreting sarcasm, slang, and other complex language nuances may prove difficult for the model.

- We may face scalability challenges given the team’s limited exposure to larger-scale system development.

- Scope creep poses a risk, potentially diverting focus and resources.

- Ensuring access to diverse and representative data to prevent bias and maintain consistent sentiment analysis will be challenging.
### **Mitigation Strategy**
- Assign clear tasks and responsibilities, while breaking the project into small, digestable portions as well as utilizing the agile practices. 

- Utilizing the project tracking software set up through trello to track tasks that need to be accomplished. Maintaining communication on an as needed basis through discord and utilize the weekly meetings to communicate updates and comcerns. 

- Begin the project using pre trained models until we are comfortable with increasing the customization. Familiarize ourselves as needed with tuorials for the relevant tools.

- Make sure the data used will encompass enough of the problematic language to accurately interperate it. Possibly provide users with a confidence flag on the interpretation. 

- Utlize clearly defined project structure and strict version controll methods to ensure that changes are accceptable on a range of machines. 

- Use clearly defined goals in the project tracking software and maintain agile practices to only do what is necessary to complete said goals. 

- Create testing for bias and use diverse and varied datasets.  
### **Development Method: Kanban**
- Tracking: 
Kanban boards will be maintained in Trello, providing a clear, real-time view of who is working on what. This is especially beneficial for our team, which operates on an asynchronous schedule, ensuring updates and progress are always visible 	regardless of time zones or availability.

- Flexibility: 
Kanban does not rely on fixed sprint cycles, which aligns well with our project’s dynamic nature. Certain components—such as model integration or tuning—may take longer than others. The flexibility of Kanban allows us to easily adjust task 	priorities, reassign responsibilities, and shift timelines as needed without disrupting overall workflow.

- Work in Progress (WIP) Limits: 
To maintain momentum and encourage consistent delivery of functionality, we will use WIP limits to reduce multitasking and context switching. The team will be encouraged to focus on resolving blockers before starting new tasks, helping us 		avoid bottlenecks and keep the board flowing smoothly.
### **Project Tracking Software Link:**
 -  https://trello.com/invite/b/6848733b249b560dbd6d56bd/ATTI24989037cb513df6cabfbf08b24fc7a9949410BC/3308-team-4
