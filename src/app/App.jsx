import LegacyMvpApp from '../App.jsx';
import { AppProviders } from './providers/AppProviders.jsx';

export default function App() {
  return (
    <AppProviders>
      <LegacyMvpApp />
    </AppProviders>
  );
}
