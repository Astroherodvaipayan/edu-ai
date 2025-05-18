import { useEffect, useRef, useState } from "react";
import { useAuth } from "../contexts/AuthContext";

const extractVideoId = (url) => {
	const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
	const match = url.match(regExp);
	return match && match[2].length === 11 ? match[2] : null;
};

const useChat = () => {
	const [messages, setMessages] = useState([]);
	const [input, setInput] = useState("");
	const [isListening, setIsListening] = useState(false);
	const [sessionId, setSessionId] = useState("");
	const messagesEndRef = useRef(null);
	const [resourceType, setResourceType] = useState("text");
	const [videos, setVideos] = useState([
		{
			title: "Quantum Computing",
			url: "https://www.youtube.com/watch?v=lt4OsgmUTGI",
		},
		{ title: "Blockchain", url: "https://www.youtube.com/watch?v=SSo_EIwHSd4" },
	]);
	const [pdfs, setPdfs] = useState([]);
	const [selectedResource, setSelectedResource] = useState(null);
	const [content, setContent] = useState("");
	const { user } = useAuth();

	console.log("content", messages);

	useEffect(() => {
		setSessionId(Math.random().toString(36).substring(7));

		const SpeechRecognition =
			window.SpeechRecognition || window.webkitSpeechRecognition;
		if (SpeechRecognition) {
			const recognition = new SpeechRecognition();
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event) => {
				const transcript = Array.from(event.results)
					.map((result) => result[0])
					.map((result) => result.transcript)
					.join("");

				setInput(transcript);
			};

			window.recognition = recognition;
		}
	}, []);

	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages]);

	const handleSend = async () => {
		if (!input.trim()) return;

		const userMessage = { type: "user", content: input };
		setMessages((prev) => [...prev, userMessage]);
		setInput("");

		try {
			// Get chat history for context
			const chatHistory = messages
				.map((msg) => `${msg.type}: ${msg.content}`)
				.join("\n");

			const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ 
					messages: [
						...messages.map(msg => ({
							role: msg.type === "user" ? "user" : "assistant",
							content: msg.content
						})),
						{ role: "user", content: input }
					],
					transcript: content,
					user_id: user?.id
				}),
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			setMessages((prev) => [
				...prev,
				{ type: "bot", content: data.message },
			]);
			setContent(data.message);
		} catch (error) {
			console.error("Error sending message:", error);
			setMessages((prev) => [
				...prev,
				{
					type: "error",
					content: "Sorry, there was an error processing your message.",
				},
			]);
			setContent("");
		}
	};

	const handleVoiceToggle = () => {
		if (isListening) {
			window.recognition?.stop();
		} else {
			window.recognition?.start();
		}
		setIsListening(!isListening);
	};

	const handleFileUpload = async (event) => {
		const file = event.target.files[0];
		if (!file) return;

		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/process-pdf`, {
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			
			if (!data.success) {
				throw new Error(data.error || "Failed to process PDF");
			}

			setMessages((prev) => [
				...prev,
				{
					type: "bot",
					content: data.transcript,
				},
				{
					type: "system",
					content: `Successfully processed ${file.name}. Here's the summary:\n\n${data.summary}`,
				},
			]);
			setPdfs((prev) => [...prev, { name: file.name }]);
			setContent(data.transcript);
		} catch (error) {
			console.error("Error processing PDF:", error);
			setMessages((prev) => [
				...prev,
				{
					type: "error",
					content: `Error processing PDF: ${error.message}`,
				},
			]);
		}
	};

	return [
		{
			messages,
			input,
			videos,
			isListening,
			messagesEndRef,
			content,
			resourceType,
			pdfs,
		},
		{
			setVideos,
			setResourceType,
			handleSend,
			handleVoiceToggle,
			setInput,
			handleFileUpload,
			setSelectedResource,
		},
	];
};

export default useChat;
