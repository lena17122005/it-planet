import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { motion } from 'framer-motion';
import type { Vacancy } from '../../types';
import { markerIcons } from '../../hooks/useMap';

interface Props {
  vacancies: Vacancy[];
  favoriteIds: string[];
  onSelect: (vacancy: Vacancy) => void;
}

export default function Map({ vacancies, favoriteIds, onSelect }: Props) {
  return (
    <MapContainer center={[55.751244, 37.618423]} zoom={5} className="h-[520px] w-full rounded-2xl">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {vacancies.map((vacancy) => {
        const icon = vacancy.type === 'event' ? markerIcons.event : favoriteIds.includes(vacancy.id) ? markerIcons.favorite : markerIcons.default;

        return (
          <Marker key={vacancy.id} position={[vacancy.lat, vacancy.lng]} icon={icon} eventHandlers={{ click: () => onSelect(vacancy) }}>
            <Popup>
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-1">
                <h3 className="font-semibold">{vacancy.title}</h3>
                <p className="text-sm text-slate-600">{vacancy.company}</p>
                <p className="text-xs text-slate-500">{vacancy.tags.join(', ')}</p>
              </motion.div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
