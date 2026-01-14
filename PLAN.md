## Design Plan
## Techstack Overview

### **Frontend**

* **Framework:** Next.js
* **Styling:** Tailwind CSS
* **Component Library:** shadcn/ui
* **Authentication:** Clerk
* **Storage:** Session Storage (Temporary Answer Storage)
* **Deployment:** Vercel

### **Backend**

* **Framework:** Flask
* **Database Library:** PyMongo
* **Deployment:** PythonAnywhere

### **Database**

* **Database:** MongoDB
* **Hosting:** MongoDB Atlas

---

## Application Requirements Assumptions

### **1. Admin Workspace (`/managequiz`)**

The admin side focuses on quiz management and visibility control.

* **Authentication:** Access is restricted via **Clerk**.
* **Quizzes:** View a list of existing quizzes and their current status (Draft/Published).

**Quiz Creation Interface:**
* **Question Text:** Standard text input.
* **Option Type:** Between **Single Choice** (Radio) or **Multiple Choice** (Checkbox).
* **Options:** Multi-tag input (restricted to a maximum of 4).
* **Answer(s):** Dynamic selection based on the inputted options to mark the correct answer(s).


**Publishing:** A "Publish" action updates the MongoDB record to make the quiz visible to users.

---

### **2. User Experience (`/quiz`)**

The user side focuses on attempting the quizzes..

**Quizzes:** A gallery view of all quizzes.

**Quiz Flow:**
* **Initialization:** Fetch full quiz data by ID from the Flask backend.
* **Persistence:** As users progress, answers are stored in **Session Storage** to prevent data loss on page refresh.
* **Submission:** On completion, the answer payload is sent to the Flask server for validation against the stored answer key.


**Results & Feedback:**
* **Scoring:** Backend returns a score and correct/incorrect breakdown.
* **Visual Cues:** Frontend applies conditional formatting (colors) based on performance thresholds (e.g., Green for , Red for ).



---

### **3. Data Flow**

| Action | Source | Target | Technology |
| --- | --- | --- | --- |
| **Create Quiz** | Frontend Form | MongoDB | Next.js → Flask → PyMongo |
| **Fetch Quizzes** | MongoDB | UI List | Flask API → Next.js  |
| **Store Progress** | User Input | Browser | Session Storage |
| **Validate Result** | Session Storage | Flask Logic | POST Request → Result Object |
