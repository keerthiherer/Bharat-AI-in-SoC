# =========================================
# Knowledge Base Module
# =========================================
import pickle
import re

class KnowledgeBase:
    def __init__(self):
        """Load all knowledge base files"""
        self.history = self._load_kb("history_kb.pkl")
        self.indian_history = self._load_kb("indian_history_kb.pkl")
        self.politics = self._load_kb("politics_kb.pkl")
        self.world_gk = self._load_kb("world_gk_kb.pkl")
        self.india_gk = self._load_kb("india_gk_kb.pkl")
    
    def _load_kb(self, filename):
        """Load pickle file"""
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except:
            return {}
    
    def search(self, query, kb_type="all"):
        """
        Search in knowledge base
        kb_type: "history", "indian_history", "politics", "world_gk", "india_gk", or "all"
        """
        query = query.lower().strip()
        results = []
        
        # Search in history
        if kb_type in ["history", "all"]:
            result = self._search_in_dict(query, self.history)
            if result:
                results.append(("history", result))
        
        # Search in indian history
        if kb_type in ["indian_history", "all"]:
            result = self._search_in_dict(query, self.indian_history)
            if result:
                results.append(("indian_history", result))
        
        # Search in politics
        if kb_type in ["politics", "all"]:
            result = self._search_in_dict(query, self.politics)
            if result:
                results.append(("politics", result))
        
        # Search in world GK
        if kb_type in ["world_gk", "all"]:
            result = self._search_in_dict(query, self.world_gk)
            if result:
                results.append(("world_gk", result))
        
        # Search in india GK
        if kb_type in ["india_gk", "all"]:
            result = self._search_in_dict(query, self.india_gk)
            if result:
                results.append(("india_gk", result))
        
        return results
    
    def _search_in_dict(self, query, kb_dict):
        """Search for exact match or partial match"""
        # Exact match
        for key, value in kb_dict.items():
            if key.lower() == query:
                return value
        
        # Partial match (substring)
        for key, value in kb_dict.items():
            if query in key.lower() or key.lower() in query:
                return value
        
        return None
    
    def get_history(self, query):
        """Get history information"""
        return self._search_in_dict(query.lower(), self.history)
    
    def get_indian_history(self, query):
        """Get Indian history information"""
        return self._search_in_dict(query.lower(), self.indian_history)
    
    def get_politics(self, query):
        """Get politics information"""
        return self._search_in_dict(query.lower(), self.politics)
    
    def get_world_gk(self, query):
        """Get world general knowledge"""
        return self._search_in_dict(query.lower(), self.world_gk)
    
    def get_india_gk(self, query):
        """Get India general knowledge"""
        return self._search_in_dict(query.lower(), self.india_gk)
    
    def format_response(self, topic, answer):
        """Format response in Hindi"""
        if answer:
            return f"{topic} के बारे में: {answer}"
        return None
