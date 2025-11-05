import api from './api';

const authService = {
  // Inscription d'un nouvel utilisateur
  register: async (username, email, password, password2) => {
    const response = await api.post('/auth/register/', {
      username,
      email,
      password,
      password2,
    });
    
    // Sauvegarde les tokens dans localStorage
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    
    return response.data;
  },

  // Connexion
  login: async (email, password) => {
    const response = await api.post('/auth/login/', {
      email,
      password,
    });
    
    // Sauvegarde les tokens
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    
    return response.data;
  },

  // Déconnexion
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // Récupère le profil utilisateur
  getProfile: async () => {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  // Vérifie si l'utilisateur est connecté
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

export default authService;