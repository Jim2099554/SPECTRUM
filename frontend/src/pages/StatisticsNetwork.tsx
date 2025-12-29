import React, { useState, useRef, useEffect } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';
import axiosInstance from '../api/axiosInstance';

// Datos mockup para grafo de vínculos
type NodeType = 'pin' | 'contact';

interface Node {
  id: string;
  label: string;
  color: string;
  type: NodeType;
  phones?: string[];  // Números de teléfono asociados a esta identidad
  identity?: string;  // Nombre real del contacto
  alias?: string;     // Alias o apodo del contacto
}

interface Link {
  source: string;
  target: string;
  value: number; // cantidad de llamadas
}

interface GraphData {
  nodes: Node[];
  links: Link[];
}


const StatisticsNetwork: React.FC = () => {
  const fgRef = useRef<any>(null);
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [loadingGraph, setLoadingGraph] = useState(true);
  const [errorGraph, setErrorGraph] = useState<string | null>(null);
  const [hoveredNode, setHoveredNode] = useState<Node | null>(null);
  // const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());

  // Cargar datos de la red desde el backend
  useEffect(() => {
    const loadNetworkData = async () => {
      try {
        const pin = localStorage.getItem('pin') || '666';
        const response = await axiosInstance.get('/network', { params: { pin } });
        setGraphData(response.data);
        setLoadingGraph(false);
      } catch (error: any) {
        setErrorGraph(error?.response?.data?.detail || 'Error al cargar la red de vínculos');
        setLoadingGraph(false);
      }
    };
    loadNetworkData();
  }, []);

  React.useEffect(() => {
    if (fgRef.current) {
      // Fija la posición inicial de la cámara
      fgRef.current.cameraPosition({ x: 0, y: 0, z: 300 });
    }
  }, []);

  const [selectedContact, setSelectedContact] = useState<Node | null>(null);
const [callSummary, setCallSummary] = useState<any[]>([]);
const [loadingSummary, setLoadingSummary] = useState(false);
const [errorSummary, setErrorSummary] = useState<string | null>(null);

  const nodeThreeObject = (node: any) => {
    // Tamaño dinámico según cantidad de llamadas
    const callCount = node.phones?.length || 1;
    const baseSize = node.type === 'pin' ? 12 : Math.min(8 + callCount * 0.5, 12);
    
    const geometry = new THREE.SphereGeometry(baseSize, 32, 32);
    
    // Colores mejorados con gradientes
    const baseColor = node.type === 'pin' ? '#ff4444' : '#4488ff';
    const borderColor = node.type === 'pin' ? '#ff0000' : '#0066ff';
    // Material con efecto metálico
    const sphereMat = new THREE.MeshPhongMaterial({ 
      color: baseColor,
      emissive: borderColor,
      emissiveIntensity: 0.2,
      shininess: 100,
      specular: 0xffffff
    });
    const sphere = new THREE.Mesh(geometry, sphereMat);
    
    // Borde con brillo
    const borderGeom = new THREE.SphereGeometry(baseSize + 1.5, 32, 32);
    const borderMat = new THREE.MeshBasicMaterial({ 
      color: borderColor, 
      transparent: true, 
      opacity: 0.4, 
      side: THREE.BackSide 
    });
    const border = new THREE.Mesh(borderGeom, borderMat);
    sphere.add(border);
    
    // Halo de brillo exterior
    const glowGeom = new THREE.SphereGeometry(baseSize + 3, 32, 32);
    const glowMat = new THREE.MeshBasicMaterial({ 
      color: borderColor, 
      transparent: true, 
      opacity: 0.15, 
      side: THREE.BackSide 
    });
    const glow = new THREE.Mesh(glowGeom, glowMat);
    sphere.add(glow);
    // Etiqueta mejorada con mejor contraste
    const labelDiameter = baseSize * 2;
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    // Solo texto grande y claro (sin fondo)
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = `bold ${node.type === 'pin' ? 170 : 100}px Inter, Arial, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 30;
    ctx.fillStyle = node.type === 'pin' ? '#ffffff' : '#e0e7ff';
    ctx.fillText(node.label, canvas.width / 2, canvas.height / 2);
    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(spriteMaterial);
    // El label se superpone levemente al nodo, siempre delante
    sprite.scale.set(labelDiameter * 2.2, labelDiameter * 0.7, 1);
    sprite.position.set(0, 0, labelDiameter * 0.7); // Z positivo para estar delante
    sphere.add(sprite);
    return sphere;
  };

  const handleNodeClick = async (node: any) => {
    setSelectedContact(node);
    setCallSummary([]);
    setErrorSummary(null);
    if (node.type === 'contact') {
      setLoadingSummary(true);
      try {
        const pin = localStorage.getItem('pin') || '666';
        
        // Si el nodo tiene múltiples números (agrupados por identidad), obtener llamadas de todos
        const phones = node.phones || [node.id];
        const allCalls: any[] = [];
        
        for (const phone of phones) {
          try {
            const response = await axiosInstance.get(`/llamadas`, {
              params: { pin, contact: phone }
            });
            allCalls.push(...response.data);
          } catch (err) {
            console.warn(`No se pudieron obtener llamadas para ${phone}`);
          }
        }
        
        // Ordenar por fecha descendente
        allCalls.sort((a, b) => {
          const dateA = new Date(a.fecha || '');
          const dateB = new Date(b.fecha || '');
          return dateB.getTime() - dateA.getTime();
        });
        
        setCallSummary(allCalls);
      } catch (error: any) {
        setErrorSummary(error?.response?.data?.detail || 'Error al obtener resumen de llamadas');
      } finally {
        setLoadingSummary(false);
      }
    }
  };

  // Forzar resize del grafo tras el primer render para evitar superposición
  React.useEffect(() => {
    if (fgRef.current && typeof fgRef.current.width === 'function') {
      setTimeout(() => {
        try {
          fgRef.current.width(fgRef.current.container.offsetWidth);
          fgRef.current.height(fgRef.current.container.offsetHeight);
        } catch {}
      }, 150);
    }
  }, []);

  // Estado para dimensiones
  const [graphSize, setGraphSize] = useState({ width: 400, height: 520 });
  const containerRef = useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    function updateSize() {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setGraphSize({ width: rect.width, height: rect.height });
      }
    }
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  return (
    <div className="flex w-full h-[600px] mt-12">
      <div ref={containerRef} className="bg-gray-50 dark:bg-gray-900 rounded-2xl h-full basis-1/2 max-w-[50vw] min-w-0 overflow-hidden flex flex-col justify-center items-center" style={{ height: 520, minHeight: 520, boxShadow: 'none', border: 'none' }}>
        {loadingGraph ? (
          <div className="text-white">Cargando red de vínculos...</div>
        ) : errorGraph ? (
          <div className="text-red-500">{errorGraph}</div>
        ) : (
        <div className="w-full h-full">
          <ForceGraph3D
            ref={fgRef}
            graphData={graphData}
            nodeAutoColorBy="type"
            backgroundColor="#0a0a0f"
            showNavInfo={false}
            controlType="orbit"
            nodeThreeObject={nodeThreeObject}
            linkColor={(link: any) => {
              if (highlightLinks.has(link)) {
                return 'rgba(255, 165, 0, 0.8)';
              }
              return hoveredNode ? 'rgba(100, 100, 100, 0.2)' : 'rgba(245, 158, 66, 0.6)';
            }}
            linkOpacity={1}
            width={graphSize.width}
            height={graphSize.height}
            onNodeClick={handleNodeClick}
            enableNodeDrag={true}
            onNodeHover={(node: any) => {
              setHoveredNode(node);
              
              // Highlight de nodos y enlaces relacionados
              if (node) {
                const neighbors = new Set();
                const links = new Set();
                
                graphData.links.forEach(link => {
                  if (link.source === node.id || (link.source as any).id === node.id) {
                    neighbors.add(typeof link.target === 'object' ? (link.target as any).id : link.target);
                    links.add(link);
                  }
                  if (link.target === node.id || (link.target as any).id === node.id) {
                    neighbors.add(typeof link.source === 'object' ? (link.source as any).id : link.source);
                    links.add(link);
                  }
                });
                
                neighbors.add(node.id);
                // setHighlightNodes(neighbors);
                setHighlightLinks(links);
              } else {
                // setHighlightNodes(new Set());
                setHighlightLinks(new Set());
              }
            }}
            nodeLabel={(node: any) => {
              const phones = node.phones?.length > 1 ? `<br/><small>📱 ${node.phones.length} números</small>` : '';
              const identity = node.identity ? `<br/><small>👤 ${node.identity}</small>` : '';
              const alias = node.alias ? `<br/><small>🏷️ ${node.alias}</small>` : '';
              return `<div style="background: rgba(0,0,0,0.8); padding: 8px 12px; border-radius: 8px; color: white; font-family: Arial;">
                <strong>${node.label}</strong>${phones}${identity}${alias}
              </div>`;
            }}
            linkWidth={(link: any) => {
              // Grosor según cantidad de llamadas
              const value = link.value || 1;
              return highlightLinks.has(link) ? Math.max(value * 0.5, 3) : Math.max(value * 0.3, 1);
            }}
            linkDirectionalParticles={(link: any) => highlightLinks.has(link) ? 4 : 0}
            linkDirectionalParticleWidth={2}
            linkDirectionalParticleSpeed={0.006}
          />
        </div>
        )}
      </div>
      <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl shadow p-6 min-h-[520px] h-full">
        {selectedContact ? (
          <div>
            {selectedContact.type === 'contact' ? (
              <>
                <h2 className="text-xl font-bold mb-2 text-white">Resumen de llamadas con {selectedContact.label}</h2>
                {selectedContact.phones && selectedContact.phones.length > 1 && (
                  <div className="mb-3 p-2 bg-blue-900/30 rounded border border-blue-700/50">
                    <p className="text-xs text-blue-300 font-semibold mb-1">📱 Números asociados:</p>
                    <div className="flex flex-wrap gap-1">
                      {selectedContact.phones.map((phone: string) => (
                        <span key={phone} className="text-xs bg-blue-800/50 text-blue-200 px-2 py-1 rounded">
                          {phone}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {loadingSummary && <div className="text-gray-400">Cargando resumen...</div>}
                {errorSummary && <div className="text-red-500">{errorSummary}</div>}
                {!loadingSummary && !errorSummary && callSummary.length === 0 && (
                  <div className="text-gray-400">No hay llamadas registradas con este contacto.</div>
                )}
                {!loadingSummary && callSummary.length > 0 && (
                  <div className="overflow-x-auto">
                    <table className="min-w-full text-sm text-left text-gray-300">
                      <thead className="bg-gray-800 text-xs uppercase">
                        <tr>
                          <th className="px-3 py-2">Fecha</th>
                          <th className="px-3 py-2">Número marcado</th>
                          <th className="px-3 py-2">Resumen</th>
                          <th className="px-3 py-2">Audio</th>
                          <th className="px-3 py-2">PDF</th>
                        </tr>
                      </thead>
                      <tbody>
                        {callSummary.map((call, idx) => (
                          <tr key={call.call_id || idx} className="border-b border-gray-700">
                            <td className="px-3 py-2 whitespace-nowrap">{call.fecha}</td>
                            <td className="px-3 py-2 whitespace-nowrap">{call.contact || call.numero_marcado || call.numero || '-'}</td>
                            <td className="px-3 py-2 max-w-[300px] truncate">{call.resumen || 'Sin resumen disponible.'}</td>
                            <td className="px-3 py-2">
                              {call.audio ? (
                                <audio controls src={call.audio} className="max-w-[120px]">Tu navegador no soporta audio</audio>
                              ) : (
                                <span className="text-gray-500">-</span>
                              )}
                            </td>
                            <td className="px-3 py-2">
                              {call.pdf ? (
                                <a href={call.pdf} target="_blank" rel="noopener noreferrer" className="text-blue-400 underline">Ver PDF</a>
                              ) : (
                                <span className="text-gray-500">-</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </>
            ) : (
              <div className="text-gray-400">Nodo seleccionado: {selectedContact.label} (tipo: {selectedContact.type})<br/>Haz clic en un nodo de contacto para ver el resumen de llamadas.</div>
            )}
          </div>
        ) : (
          <div className="text-gray-500">Haz clic en un nodo de contacto para ver el resumen de llamadas.</div>
        )}
      </div>
    </div>
  );
};

export default StatisticsNetwork;
