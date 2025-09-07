# AgroPulse - Frontend Application 🌱

This is the frontend for the AgroPulse application, a farmer-friendly platform built with React for HackOdisha 5.0. It provides an intuitive interface for farmers to get AI-powered crop recommendations and track their progress.

---

## ✨ Key Features

-   **Secure Authentication**: User sign-up and login handled by **Supabase**.
-   **AI Crop Recommendation**: An easy-to-use form to input farm data and get instant predictions.
-   **Visual Result Card**: Displays the recommended crop with its **image** and a confidence score.
-   **Gamified Dashboard**: Shows progress, badges, and a local leaderboard to encourage engagement.
-   **Multilingual Support**: Interface available in **English, Hindi, and Odia**.
-   **Offline First**: Uses a Service Worker to cache app data for offline accessibility.
-   **Responsive Design**: Mobile-first UI that works beautifully on any device.

---

## 🛠️ Tech Stack

-   **React**: JavaScript library for building user interfaces.
-   **Vite**: Next-generation frontend tooling for a fast development experience.
-   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
-   **Supabase**: For user authentication and session management.
-   **Axios**: For making API calls to the backend.
-   **react-i18next**: For internationalization and language support.

---

## 🚀 Getting Started

### Prerequisites

-   Node.js (v18 or higher recommended)
-   A Supabase account (for authentication keys).

### Installation & Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Set up Environment Variables:**
    -   Create a new file in the `frontend` root directory named `.env.local`.
    -   Add your Supabase API keys to this file. You can get these from your Supabase project dashboard under `Settings > API`.
    ```
    VITE_SUPABASE_URL=YOUR_PROJECT_URL_HERE
    VITE_SUPABASE_ANON_KEY=YOUR_ANON_KEY_HERE
    ```

4.  **Add Crop Images:**
    -   In the `frontend/public` directory, create a new folder named `images`.
    -   Place your crop image files (e.g., `rice.jpg`, `maize.jpg`, `cotton.jpg`) inside this folder. The application will load these images dynamically.

5.  **Run the development server:**
    ```bash
    npm run dev
    ```

The application will be available at `http://localhost:5173` (or another port if 5173 is busy).