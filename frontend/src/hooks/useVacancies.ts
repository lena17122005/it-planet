import { useMemo, useState } from 'react';
import type { Vacancy, VacancyFilters } from '../types';

const mockVacancies: Vacancy[] = [
  {
    id: '1',
    title: 'Frontend Intern',
    company: 'Tech Start',
    city: 'Москва',
    address: 'Москва, ул. Льва Толстого, 16',
    description: 'Разработка компонентов и UI фичей для продуктовой команды.',
    requirements: 'React, TypeScript, REST',
    salaryFrom: 60000,
    salaryTo: 90000,
    lat: 55.751244,
    lng: 37.618423,
    format: 'hybrid',
    type: 'internship',
    tags: ['React', 'TypeScript']
  },
  {
    id: '2',
    title: 'Backend Junior',
    company: 'Cloud Group',
    city: 'Санкт-Петербург',
    address: 'Санкт-Петербург, Невский проспект, 28',
    description: 'Поддержка FastAPI-сервисов и интеграций.',
    salaryFrom: 90000,
    salaryTo: 140000,
    lat: 59.9343,
    lng: 30.3351,
    format: 'office',
    type: 'vacancy',
    tags: ['Python', 'FastAPI', 'PostgreSQL']
  },
  {
    id: '3',
    title: 'Career Meetup: ML в 2026',
    company: 'AI Community',
    city: 'Казань',
    address: 'Казань, ул. Баумана, 44',
    description: 'Оффлайн мероприятие с карьерным блоком и нетворкингом.',
    eventDate: '2026-04-18',
    lat: 55.7961,
    lng: 49.1064,
    format: 'office',
    type: 'event',
    tags: ['ML', 'Career', 'Networking']
  }
];

const DEFAULT_FILTERS: VacancyFilters = {
  query: '',
  city: '',
  salaryFrom: undefined,
  salaryTo: undefined,
  format: 'all',
  tags: ''
};

export function useVacancies() {
  const [filters, setFilters] = useState<VacancyFilters>(DEFAULT_FILTERS);

  const vacancies = useMemo(() => {
    const tagList = filters.tags
      .split(',')
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);

    return mockVacancies.filter((vacancy) => {
      const inQuery =
        !filters.query ||
        vacancy.title.toLowerCase().includes(filters.query.toLowerCase()) ||
        vacancy.company.toLowerCase().includes(filters.query.toLowerCase());

      const inCity = !filters.city || vacancy.city.toLowerCase().includes(filters.city.toLowerCase());
      const inFormat = filters.format === 'all' || vacancy.format === filters.format;
      const inSalaryFrom = !filters.salaryFrom || (vacancy.salaryFrom ?? 0) >= filters.salaryFrom;
      const inSalaryTo = !filters.salaryTo || (vacancy.salaryTo ?? Number.MAX_SAFE_INTEGER) <= filters.salaryTo;
      const inTags = !tagList.length || tagList.every((tag) => vacancy.tags.map((t) => t.toLowerCase()).includes(tag));

      return inQuery && inCity && inFormat && inSalaryFrom && inSalaryTo && inTags;
    });
  }, [filters]);

  return {
    vacancies,
    filters,
    setFilters
  };
}
