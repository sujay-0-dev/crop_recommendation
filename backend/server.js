// server.js

const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// --- Simple Mock Database for Dashboard Data ---
const users = {
  "1234": {
    name: "Farmer John",
    language: "en",
    badges: { firstHarvest: true, savedWater: false, pestControlPro: true },
    progress: { currentStage: "Harvest Ready", completion: 90 },
    farmData: []
  }
};

const leaderboard = [
  { name: "Suresh K.", yield: 1500, region: "Bhubaneswar" },
  { name: "Priya M.", yield: 1450, region: "Cuttack" },
  { name: "Anjali S.", yield: 1380, region: "Puri" },
];

const advisories = {
  en: "Weather alert: Expect light showers this afternoon. Ensure proper drainage for young crops.",
  hi: "मौसम चेतावनी: आज दोपहर हल्की बारिश की उम्मीद है। युवा फसलों के लिए उचित जल निकासी सुनिश्चित करें।",
  or: "ପାଣିପାଗ ସତର୍କତା: ଆଜି ଅପରାହ୍ନରେ ସାମାନ୍ୟ ବର୍ଷା ହେବାର ସମ୍ଭାବନା ଅଛି। ଯୁବ ଫସଲ ପାଇଁ ଉପଯୁକ୍ତ ଜଳ ନିଷ୍କାସନ ସୁନିଶ୍ଚିତ କରନ୍ତୁ।"
};
// --------------------------------------------------

// --- API Endpoints ---

// Endpoint for simple PIN login (can be kept for fallback or removed if only using Supabase)
app.post('/api/login', (req, res) => {
  const { pin } = req.body;
  if (users[pin]) {
    res.status(200).json({ success: true, user: users[pin] });
  } else {
    res.status(401).json({ success: false, message: "Invalid PIN" });
  }
});

// Endpoint to serve data for the Dashboard
app.get('/api/dashboard', (req, res) => {
  res.status(200).json({ leaderboard, advisories });
});

// The main endpoint for Crop Recommendation
app.post('/api/recommend', async (req, res) => {
  // The URL of your friend's deployed model
  const modelUrl = 'https://crop-recommender-231842036638.asia-south1.run.app/predict';

  try {
    console.log(`➡️  Sending request to model at ${modelUrl} with data:`, req.body);
    
    // Call the external model API
    const response = await axios.post(modelUrl, req.body);
    
    console.log('✅ Received successful response from model:', response.data);

    // Check if the expected key exists before sending
    if (!response.data || !response.data.predicted_crop) {
      throw new Error("Model response is valid but missing the 'predicted_crop' key.");
    }
    
    // **Important:** Send the entire data object from the model back to the frontend.
    // This allows the frontend to access `predicted_crop`, `confidence`, etc.
    res.status(200).json(response.data); 
    
  } catch (error) {
    console.error("❌ Error connecting to the model API!");

    if (error.response) {
      // The model's server responded with an error status (4xx or 5xx)
      console.error("Status:", error.response.status);
      console.error("Data:", error.response.data);
      res.status(502).json({ 
        message: "The prediction service is reporting an error.",
        details: `Model service responded with status: ${error.response.status}.`
      });
    } else if (error.request) {
      // The request was made but no response was received
      console.error("Request Error:", error.request);
      res.status(504).json({ 
        message: "Could not connect to the prediction service.",
        details: "No response was received from the model's server. It might be offline."
      });
    } else {
      // Something else went wrong (like the key mismatch error we fixed)
      console.error("General Error:", error.message);
      res.status(500).json({ 
        message: "An internal server error occurred.",
        details: error.message 
      });
    }
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});