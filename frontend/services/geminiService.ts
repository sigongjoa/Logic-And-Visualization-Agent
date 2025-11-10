
import { GoogleGenAI, Type } from "@google/genai";

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  // In a real app, you might want to handle this more gracefully.
  // For this context, we assume the key is always available.
  console.warn("API_KEY environment variable not set. Gemini API calls will fail.");
}

const ai = new GoogleGenAI({ apiKey: API_KEY! });

export const generateFeedback = async (submissionText: string): Promise<{ feedback: string, score: number }> => {
  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: `You are a helpful and constructive coach providing feedback on a student's assignment about 'UX Design Principles'. The student's submission is below.
      Please provide thoughtful, encouraging, and constructive feedback. Also, provide a suggested score out of 100.
      
      --- STUDENT SUBMISSION ---
      ${submissionText}
      --- END SUBMISSION ---
      
      Return the feedback and score in JSON format.
      `,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            feedback: {
              type: Type.STRING,
              description: "Constructive feedback for the student's submission.",
            },
            score: {
              type: Type.INTEGER,
              description: "A suggested score for the assignment, from 0 to 100.",
            },
          },
          required: ["feedback", "score"],
        },
        temperature: 0.7,
      },
    });

    const jsonString = response.text.trim();
    const parsedResponse = JSON.parse(jsonString);
    
    return {
      feedback: parsedResponse.feedback || "Could not generate feedback.",
      score: parsedResponse.score || 0,
    };

  } catch (error) {
    console.error("Error generating feedback with Gemini API:", error);
    return {
      feedback: "There was an error generating AI feedback. Please try again or write your own.",
      score: 0,
    };
  }
};
