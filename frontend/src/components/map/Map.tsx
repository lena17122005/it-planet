import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { motion } from 'framer-motion';
import type { Vacancy } from '../../types';
import { vacancyIcon } from '../../hooks/useMap';

interface Props {
  vacancies: Vacancy[];
}

export default function Map({ vacancies }: Props) {
  return (
    <MapContainer center={[55.751244, 37.618423]} zoom={10} className="h-[420px] w-full rounded-xl">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {vacancies.map((vacancy) => (
        <Marker key={vacancy.id} position={[vacancy.lat, vacancy.lng]} icon={vacancyIcon}>
          <Popup>
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-1">
              <h3 className="font-semibold">{vacancy.title}</h3>
              <p className="text-sm text-slate-600">{vacancy.company}</p>
              <p className="text-sm">{vacancy.tags.join(', ')}</p>
            </motion.div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
