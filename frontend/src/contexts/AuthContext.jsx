"use client";

import { createContext, useContext, useEffect, useState } from "react";
import supabase from "../lib/supabase";

// Create the authentication context
const AuthContext = createContext();

// Custom hook to use the authentication context
export const useAuth = () => {
	return useContext(AuthContext);
};

// Authentication provider component
export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);
	const [isTestAccount, setIsTestAccount] = useState(false);
	const [authError, setAuthError] = useState(null);

	// Check for user session on initial load
	useEffect(() => {
		const checkUser = async () => {
			try {
				// Check if Supabase is not available
				if (!supabase) {
					console.error("Supabase client is not available - check your environment variables");
					setAuthError("Authentication service not available - check environment variables");
					setLoading(false);
					return;
				}

				// Get the current session
				const {
					data: { session },
					error: sessionError,
				} = await supabase.auth.getSession();

				if (sessionError) {
					console.error("Error getting session:", sessionError);
					setAuthError("Error connecting to authentication service");
				} else {
					// Set the user if there's a session
					setUser(session?.user || null);
					setIsTestAccount(session?.user?.email === "test@ved-ai.com");
					setAuthError(null);
				}
			} catch (error) {
				console.error("Error checking user session:", error);
				setAuthError("Authentication service error");
			} finally {
				setLoading(false);
			}
		};

		checkUser();

		// Listen for authentication state changes
		if (supabase) {
			const {
				data: { subscription },
			} = supabase.auth.onAuthStateChange((event, session) => {
				console.log("Auth state changed:", event);
				setUser(session?.user || null);
				setIsTestAccount(session?.user?.email === "test@ved-ai.com");
				setLoading(false);
			});

			// Clean up the subscription when the component unmounts
			return () => {
				subscription.unsubscribe();
			};
		}
	}, []);

	// Sign up function
	const signUp = async (email, password) => {
		if (!supabase) {
			console.error("Supabase client is not available for signup");
			return {
				data: null,
				error: new Error("Authentication service not available - check environment variables"),
			};
		}

		try {
			console.log("Attempting signup for:", email);
			// Use signUpWithPassword instead of signUp to ensure proper user creation
			const { data, error } = await supabase.auth.signUp({
				email,
				password,
				options: {
					// This ensures the user is created in the auth.users table
					emailRedirectTo: `${window.location.origin}/login`,
					// Add any additional user metadata if needed
					data: {
						created_at: new Date().toISOString(),
					},
				},
			});

			if (error) throw error;
			return { data, error: null };
		} catch (error) {
			console.error("Signup error:", error);
			return { data: null, error };
		}
	};

	// Sign in function
	const signIn = async (email, password) => {
		if (!supabase) {
			console.error("Supabase client is not available for signin");
			return {
				data: null,
				error: new Error("Authentication service not available - check environment variables"),
			};
		}

		try {
			console.log("Attempting signin for:", email);
			const { data, error } = await supabase.auth.signInWithPassword({
				email,
				password,
			});

			if (error) throw error;
			return { data, error: null };
		} catch (error) {
			console.error("Signin error:", error);
			return { data: null, error };
		}
	};

	// Sign out function
	const signOut = async () => {
		if (!supabase) {
			console.error("Supabase client is not available for signout");
			return { error: new Error("Authentication service not available - check environment variables") };
		}

		try {
			const { error } = await supabase.auth.signOut();
			if (error) throw error;
			return { error: null };
		} catch (error) {
			console.error("Signout error:", error);
			return { error };
		}
	};

	// Reset password function
	const resetPassword = async (email) => {
		if (!supabase) {
			console.error("Supabase client is not available for password reset");
			return {
				data: null,
				error: new Error("Authentication service not available - check environment variables"),
			};
		}

		try {
			const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
				redirectTo: `${window.location.origin}/login`,
			});
			if (error) throw error;
			return { data, error: null };
		} catch (error) {
			console.error("Reset password error:", error);
			return { data: null, error };
		}
	};

	// Update password function
	const updatePassword = async (newPassword) => {
		if (!supabase) {
			console.error("Supabase client is not available for password update");
			return {
				data: null,
				error: new Error("Authentication service not available - check environment variables"),
			};
		}

		try {
			const { data, error } = await supabase.auth.updateUser({
				password: newPassword,
			});
			if (error) throw error;
			return { data, error: null };
		} catch (error) {
			console.error("Update password error:", error);
			return { data: null, error };
		}
	};

	// Value object to be provided by the context
	const value = {
		user,
		loading,
		isTestAccount,
		authError,
		signUp,
		signIn,
		signOut,
		resetPassword,
		updatePassword,
	};

	return (
		<AuthContext.Provider value={value}>
			{!loading && children}
		</AuthContext.Provider>
	);
};