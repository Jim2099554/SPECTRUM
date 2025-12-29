import React, { useEffect, useState } from "react";
import axios from "../api/axiosInstance";

interface User {
  id: number;
  email: string;
  is_admin: boolean;
}

const UserTable: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedUser, setSelectedUser] = useState<number | null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newIsAdmin, setNewIsAdmin] = useState(false);
  const [addError, setAddError] = useState("");

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.get<User[]>("/users");
      setUsers(res.data);
    } catch (e) {
      setError("Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async () => {
    if (!selectedUser) return;
    try {
      await axios.delete(`/users/${selectedUser}`);
      setUsers(users.filter((u) => u.id !== selectedUser));
      setSelectedUser(null);
    } catch (e) {
      setError("No se pudo eliminar el usuario");
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddError("");
    try {
      const res = await axios.post<User>("/users", {
        id: 0, // El backend asigna el ID
        email: newEmail,
        is_admin: newIsAdmin,
      });
      setUsers([...users, res.data]);
      setShowAdd(false);
      setNewEmail("");
      setNewIsAdmin(false);
    } catch (e: any) {
      setAddError(e.response?.data?.detail || "No se pudo agregar el usuario");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-black dark:text-white">Usuarios registrados</h2>
        <button
          className="px-4 py-2 bg-brand-500 text-white rounded hover:bg-brand-600"
          onClick={() => setShowAdd(true)}
        >
          <span className="text-black dark:text-white">+ Agregar usuario</span>
        </button>
      </div>
      {loading ? (
        <div>Cargando...</div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <table className="min-w-full bg-white dark:bg-gray-900 rounded-xl overflow-hidden text-black dark:text-white">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-700">
              <th className="py-2 px-4 text-left text-black dark:text-white">Email</th>
              <th className="py-2 px-4 text-left text-black dark:text-white">Rol</th>
              <th className="py-2 px-4 text-center text-black dark:text-white">Seleccionar</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr
                key={user.id}
                className={
                  selectedUser === user.id
                    ? "bg-brand-50 dark:bg-brand-900"
                    : ""
                }
              >
                <td className="py-2 px-4">{user.email}</td>
                <td className="py-2 px-4 text-black dark:text-white">
                  {user.is_admin ? "Administrador" : "Usuario"}
                </td>
                <td className="py-2 px-4 text-center">
                  <input
                    type="radio"
                    name="selectedUser"
                    checked={selectedUser === user.id}
                    onChange={() => setSelectedUser(user.id)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div className="flex gap-2 mt-4">
        <button
          className="px-4 py-2 bg-red-500 text-white rounded disabled:opacity-50"
          disabled={!selectedUser}
          onClick={handleDelete}
        >
          Eliminar usuario seleccionado
        </button>
      </div>
      {/* Modal para agregar usuario */}
      {showAdd && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white dark:bg-gray-900 p-6 rounded-xl w-full max-w-sm shadow-lg">
            <h3 className="text-lg font-bold mb-4 text-black dark:text-white">Agregar nuevo usuario</h3>
            <form onSubmit={handleAdd} className="space-y-4">
              <div>
                <label className="block text-sm mb-1 text-black dark:text-white">Email</label>
                <input
                  type="email"
                  className="w-full border px-3 py-2 rounded"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm mb-1 text-black dark:text-white">Rol</label>
                <select
                  className="w-full border px-3 py-2 rounded dark:text-white text-black"
                  value={newIsAdmin ? "admin" : "user"}
                  onChange={(e) => setNewIsAdmin(e.target.value === "admin")}
                >
                  <option value="user" className="dark:text-white text-black">Usuario</option>
                  <option value="admin" className="dark:text-white text-black">Administrador</option>
                </select>
              </div>
              {addError && <div className="text-red-500 text-sm">{addError}</div>}
              <div className="flex gap-2 mt-2">
                <button
                  type="submit"
                  className="px-4 py-2 bg-brand-500 text-white rounded hover:bg-brand-600"
                >
                  Guardar
                </button>
                <button
                  type="button"
                  className="px-4 py-2 bg-gray-300 rounded"
                  onClick={() => setShowAdd(false)}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserTable;
