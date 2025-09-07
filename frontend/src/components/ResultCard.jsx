// src/components/ResultCard.jsx

import React from 'react';

const ResultCard = ({ recommendation, onReset }) => {
  // recommendation is now the full object from the backend, e.g., { predicted_crop: 'rice', confidence: 0.98 }
  const cropName = recommendation.predicted_crop;
  const confidence = (recommendation.confidence * 100).toFixed(1);

  // Dynamically create the image path based on the crop name
  const imageUrl = `/images/${cropName.toLowerCase()}.jpg`;

  return (
    <div className="max-w-md mx-auto my-8 bg-white rounded-2xl shadow-2xl overflow-hidden animate-fade-in">
      <img 
        className="w-full h-56 object-cover" 
        src={imageUrl} 
        alt={cropName} 
        // Fallback in case an image is missing
        onError={(e) => { e.target.onerror = null; e.target.src="/images/default.jpg" }}
      />
      <div className="p-6">
        <p className="text-sm font-semibold text-gray-500">BEST CROP TO SOW</p>
        <h1 className="text-5xl font-bold text-green-800 capitalize mt-2">{cropName}</h1>
        
        <div className="mt-6">
          <p className="font-medium text-gray-600">Prediction Confidence</p>
          <div className="w-full bg-gray-200 rounded-full h-4 mt-2">
            <div
              className="bg-green-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${confidence}%` }}
            ></div>
          </div>
          <p className="text-right font-bold text-green-600 mt-1">{confidence}%</p>
        </div>
        
        <button
          onClick={onReset}
          className="w-full mt-8 py-3 font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700"
        >
          Start New Analysis
        </button>
      </div>
    </div>
  );
};

export default ResultCard;