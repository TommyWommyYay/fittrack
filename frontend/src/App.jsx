import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './ProtectedRoute'
import AdminRoute from './AdminRoute'

import Home from './pages/Home'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import AdminDashboard from './pages/AdminDashboard'
import Exercises from './pages/Exercises'
import AddExercise from './pages/AddExercise'
import EditExercise from './pages/EditExercise'
import Workouts from './pages/Workouts'
import AddWorkout from './pages/AddWorkout'
import EditWorkout from './pages/EditWorkout'
import Users from './pages/Users'
import NotAuthorised from './pages/NotAuthorised'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <Layout>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Regular user routes */}
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/exercises" element={<ProtectedRoute><Exercises /></ProtectedRoute>} />
        <Route path="/workouts" element={<ProtectedRoute><Workouts /></ProtectedRoute>} />
        <Route path="/workouts/add" element={<ProtectedRoute><AddWorkout /></ProtectedRoute>} />
        <Route path="/workouts/edit/:id" element={<ProtectedRoute><EditWorkout /></ProtectedRoute>} />

        {/* Admin-only routes */}
        <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
        <Route path="/admin/users" element={<AdminRoute><Users /></AdminRoute>} />
        <Route path="/exercises/add" element={<AdminRoute><AddExercise /></AdminRoute>} />
        <Route path="/exercises/edit/:id" element={<AdminRoute><EditExercise /></AdminRoute>} />

        {/* Error pages */}
        <Route path="/not-authorised" element={<NotAuthorised />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}
