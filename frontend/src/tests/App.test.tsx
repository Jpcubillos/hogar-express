import React from 'react';
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../app/App';

describe('Hogar Express Application Bootstrapping', () => {
  it('renders loading screen initially', () => {
    const { getByText } = render(<App />);
    expect(getByText(/Cargando Hogar Express.../i)).toBeInTheDocument();
  });
});
