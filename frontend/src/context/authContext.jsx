import { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';

// Crée le contexte d'authentification
const AuthContext = createContext();

// Hook personnalisé pour utiliser le contexte facilement
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth doit être utilisé dans un AuthProvider');
  }
  return context;
};

// Provider qui enveloppe l'application
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Au chargement, vérifie si l'utilisateur est connecté
  useEffect(() => {
    const loadUser = async () => {
      if (authService.isAuthenticated()) {
        try {
          const userData = await authService.getProfile();
          setUser(userData);
        } catch (error) {
          console.error('Erreur lors du chargement du profil:', error);
          authService.logout();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  // Fonction de connexion
  const login = async (email, password) => {
    const data = await authService.login(email, password);
    const userData = await authService.getProfile();
    setUser(userData);
    return data;
  };

  // Fonction d'inscription
  const register = async (username, email, password, password2) => {
    const data = await authService.register(username, email, password, password2);
    setUser(data.user);
    return data;
  };

  // Fonction de déconnexion
  const logout = () => {
    authService.logout();
    setUser(null);
  };

  // Valeurs exposées aux composants enfants
  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};