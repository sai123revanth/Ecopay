export default async function handler(req, res) {
    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed. Use POST.' });
    }

    const { message } = req.body;

    // Check if the message is provided
    if (!message) {
        return res.status(400).json({ error: 'Message is required' });
    }

    // Retrieve your Groq API key from Vercel Environment Variables
    const apiKey = process.env.Chat_API;

    if (!apiKey) {
        return res.status(500).json({ error: 'Server Configuration Error: Chat_API environment variable is missing.' });
    }

    // Context / System Prompt - Instructing the AI on its role, language, and dataset.
    // NOTE: In a full production app, you would dynamically inject the user's actual 
    // transaction dataset data into this system prompt. For now, we establish the context.
    const systemPrompt = `
You are "Ecopay AI", a highly intelligent, polite, and helpful sustainability & financial assistant built by Team HyperOPS.
Your purpose is to help users understand their transaction datasets, calculate their carbon footprints, and offer insights on reducing their eco-impact.

CRITICAL INSTRUCTION: You MUST support major Indian languages natively. If the user asks a question in Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, or any other Indian language, you MUST reply fluently in that exact same language.

Context regarding the User's Dataset (Use this to answer data-specific questions):
- The user's dataset contains their recent banking transactions categorized by Merchant Category Code (MCC).
- The platform translates these transactions into Carbon Emissions (kg CO2e).
- If they ask general questions about their dataset, let them know you are actively analyzing their Ecopay profile to find areas where they can offset their carbon footprint (e.g., flights, gas, heavy retail).

Keep your responses concise, easy to read, and formatted neatly. Use emojis sparingly but effectively (e.g., 🌱, 💡).
`;

    try {
        // Call the Groq API utilizing the OpenAI compatible endpoint
        const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'llama-3.1-8b-instant',
                messages: [
                    { role: 'system', content: systemPrompt },
                    { role: 'user', content: message }
                ],
                temperature: 0.7,
                max_tokens: 1024
            })
        });

        const data = await response.json();

        // Handle errors returned directly from Groq
        if (!response.ok) {
            console.error("Groq API Error:", data);
            return res.status(response.status).json({ error: data.error?.message || 'Failed to fetch from Groq API' });
        }

        // Extract the reply and send back to frontend
        const aiReply = data.choices[0].message.content;
        return res.status(200).json({ reply: aiReply });

    } catch (error) {
        console.error("Backend Execution Error:", error);
        return res.status(500).json({ error: 'An internal server error occurred' });
    }
}