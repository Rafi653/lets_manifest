import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import Dashboard from '../pages/Dashboard';
import Goals from '../pages/Goals';
import LifeGoals from '../pages/LifeGoals';
import Habits from '../pages/Habits';
import Food from '../pages/Food';
import Workouts from '../pages/Workouts';
import Review from '../pages/Review';
import Blog from '../pages/Blog';
import Progress from '../pages/Progress';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'goals',
        element: <Goals />,
      },
      {
        path: 'life-goals',
        element: <LifeGoals />,
      },
      {
        path: 'habits',
        element: <Habits />,
      },
      {
        path: 'food',
        element: <Food />,
      },
      {
        path: 'workouts',
        element: <Workouts />,
      },
      {
        path: 'review',
        element: <Review />,
      },
      {
        path: 'blog',
        element: <Blog />,
      },
      {
        path: 'progress',
        element: <Progress />,
      },
    ],
  },
]);

const AppRouter = () => {
  return <RouterProvider router={router} />;
};

export default AppRouter;
