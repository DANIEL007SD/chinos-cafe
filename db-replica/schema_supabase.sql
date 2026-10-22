-- ====================================================================
-- ESQUEMA DE BASE DE DATOS RÉPLICA EN SUPABASE (POSTGRESQL)
-- Proyecto: CHINOS CAFÉ S.A. - Examen Parcial 2
-- ====================================================================
-- Copia y ejecuta este script en el "SQL Editor" de tu proyecto Supabase.
-- ====================================================================

-- 1. Tabla de réplica de Pedidos (idéntica a pedido_replica en replication.py)
CREATE TABLE IF NOT EXISTS public.pedido_replica (
    id INTEGER PRIMARY KEY,
    cliente TEXT NOT NULL,
    correo_cliente TEXT NOT NULL,
    pizza TEXT,
    refresco TEXT,
    cantidad INTEGER DEFAULT 1,
    retiro_en_sitio INTEGER DEFAULT 1,
    total DOUBLE PRECISION DEFAULT 0.0,
    estado TEXT DEFAULT 'PENDIENTE',
    fecha TEXT,
    replicado_en TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabla de réplica de Pagos (idéntica a pago_replica en replication.py)
CREATE TABLE IF NOT EXISTS public.pago_replica (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER REFERENCES public.pedido_replica(id) ON DELETE CASCADE,
    metodo TEXT DEFAULT 'YAPPY',
    referencia TEXT,
    monto DOUBLE PRECISION DEFAULT 0.0,
    fecha TEXT,
    replicado_en TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Configurar permisos y Row Level Security (RLS)
ALTER TABLE public.pedido_replica ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pago_replica ENABLE ROW LEVEL SECURITY;

-- Permitir lectura y escritura para sincronización de la réplica
DROP POLICY IF EXISTS "Acceso replica pedidos" ON public.pedido_replica;
CREATE POLICY "Acceso replica pedidos" ON public.pedido_replica
    FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Acceso replica pagos" ON public.pago_replica;
CREATE POLICY "Acceso replica pagos" ON public.pago_replica
    FOR ALL USING (true) WITH CHECK (true);
