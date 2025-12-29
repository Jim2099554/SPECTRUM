import { useEffect, useState } from "react";
import axios from "../../api/axiosInstance";

interface DangerousWord {
  id: number;
  word: string;
  category: string;
  added_date: string;
}

export default function DangerousWords() {
  const [words, setWords] = useState<DangerousWord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedWord, setSelectedWord] = useState<number | null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [newWord, setNewWord] = useState("");
  const [newCategory, setNewCategory] = useState("general");
  const [addError, setAddError] = useState("");

  const fetchWords = async () => {
    setLoading(true);
    try {
      const res = await axios.get<DangerousWord[]>("/dangerous-words");
      setWords(res.data);
    } catch (e) {
      setError("Error al cargar palabras peligrosas");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWords();
  }, []);

  const handleDelete = async () => {
    if (!selectedWord) return;
    try {
      await axios.delete(`/dangerous-words/${selectedWord}`);
      setWords(words.filter((w) => w.id !== selectedWord));
      setSelectedWord(null);
    } catch (e) {
      setError("No se pudo eliminar la palabra");
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddError("");
    if (!newWord.trim()) {
      setAddError("La palabra/frase no puede estar vacía");
      return;
    }
    try {
      const res = await axios.post<DangerousWord>("/dangerous-words", null, {
        params: {
          word: newWord.trim(),
          category: newCategory,
        },
      });
      setWords([...words, res.data]);
      setShowAdd(false);
      setNewWord("");
      setNewCategory("general");
    } catch (e: any) {
      setAddError(e.response?.data?.detail || "No se pudo agregar la palabra");
    }
  };

  return (
    <div className="rounded-2xl border border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-gray-900">
      <div className="px-5 pt-5 shadow-default rounded-2xl pb-6 bg-gray-50 dark:bg-gray-900 sm:px-6 sm:pt-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Directorio de Palabras Peligrosas
          </h3>
          <button
            className="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors"
            onClick={() => setShowAdd(true)}
          >
            + Agregar palabra
          </button>
        </div>

        {loading ? (
          <div className="text-center py-6 text-gray-500 dark:text-gray-400">Cargando...</div>
        ) : error ? (
          <div className="text-center py-6 text-red-500">{error}</div>
        ) : (
          <div className="space-y-4">
            <div className="max-h-64 overflow-y-auto">
              <table className="min-w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
                <thead className="bg-gray-100 dark:bg-gray-700 sticky top-0">
                  <tr>
                    <th className="py-2 px-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                      Palabra/Frase
                    </th>
                    <th className="py-2 px-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                      Categoría
                    </th>
                    <th className="py-2 px-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                      Fecha
                    </th>
                    <th className="py-2 px-3 text-center text-sm font-semibold text-gray-700 dark:text-gray-200">
                      Seleccionar
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {words.map((word) => (
                    <tr
                      key={word.id}
                      className={`border-t border-gray-200 dark:border-gray-700 ${
                        selectedWord === word.id
                          ? "bg-red-50 dark:bg-red-900/20"
                          : "hover:bg-gray-50 dark:hover:bg-gray-700/50"
                      }`}
                    >
                      <td className="py-2 px-3 text-sm text-gray-800 dark:text-gray-200 font-medium">
                        {word.word}
                      </td>
                      <td className="py-2 px-3 text-sm text-gray-600 dark:text-gray-400">
                        <span className="px-2 py-1 bg-gray-200 dark:bg-gray-700 rounded text-xs">
                          {word.category}
                        </span>
                      </td>
                      <td className="py-2 px-3 text-sm text-gray-600 dark:text-gray-400">
                        {word.added_date}
                      </td>
                      <td className="py-2 px-3 text-center">
                        <input
                          type="radio"
                          name="selectedWord"
                          checked={selectedWord === word.id}
                          onChange={() => setSelectedWord(word.id)}
                          className="cursor-pointer"
                        />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex gap-2 pt-2">
              <button
                className="px-4 py-2 bg-red-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-red-600 transition-colors text-sm font-medium"
                disabled={!selectedWord}
                onClick={handleDelete}
              >
                Eliminar seleccionada
              </button>
            </div>
          </div>
        )}

        {showAdd && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl w-full max-w-md shadow-2xl">
              <h3 className="text-lg font-bold mb-4 text-gray-800 dark:text-white">
                Agregar palabra/frase peligrosa
              </h3>
              <form onSubmit={handleAdd} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                    Palabra o frase
                  </label>
                  <input
                    type="text"
                    className="w-full border border-gray-300 dark:border-gray-600 px-3 py-2 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    value={newWord}
                    onChange={(e) => setNewWord(e.target.value)}
                    placeholder="Ej: amenaza, extorsión, fuga..."
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                    Categoría
                  </label>
                  <select
                    className="w-full border border-gray-300 dark:border-gray-600 px-3 py-2 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    value={newCategory}
                    onChange={(e) => setNewCategory(e.target.value)}
                  >
                    <option value="general">General</option>
                    <option value="violencia">Violencia</option>
                    <option value="narcóticos">Narcóticos</option>
                    <option value="seguridad">Seguridad</option>
                    <option value="extorsión">Extorsión</option>
                    <option value="amenazas">Amenazas</option>
                  </select>
                </div>
                {addError && <div className="text-red-500 text-sm">{addError}</div>}
                <div className="flex gap-2 mt-4">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
                  >
                    Guardar
                  </button>
                  <button
                    type="button"
                    className="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-white rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
                    onClick={() => {
                      setShowAdd(false);
                      setNewWord("");
                      setNewCategory("general");
                      setAddError("");
                    }}
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
