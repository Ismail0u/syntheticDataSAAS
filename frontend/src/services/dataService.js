import api from './api';

const dataService = {
  // Génère des données synthétiques
  generateData: async (schema, rows, format = 'json', saveSchema = false, schemaName = '') => {
    const response = await api.post('/generate/', {
      schema,
      rows,
      format,
      save_schema: saveSchema,
      schema_name: schemaName,
    }, {
      responseType: format === 'xlsx' ? 'blob' : 'text', // Pour Excel on a besoin de blob
    });
    
    return response;
  },

  // Récupère la liste des schémas sauvegardés
  getSchemas: async () => {
    const response = await api.get('/schemas/');
    return response.data;
  },

  // Crée un nouveau schéma
  createSchema: async (name, schemaJson) => {
    const response = await api.post('/schemas/', {
      name,
      schema_json: schemaJson,
    });
    return response.data;
  },

  // Supprime un schéma
  deleteSchema: async (id) => {
    const response = await api.delete(`/schemas/${id}/`);
    return response.data;
  },

  // Récupère l'historique des datasets
  getHistory: async () => {
    const response = await api.get('/history/');
    return response.data;
  },

  // Supprime un dataset de l'historique
  deleteDataset: async (id) => {
    const response = await api.delete(`/history/${id}/`);
    return response.data;
  },
};

export default dataService;