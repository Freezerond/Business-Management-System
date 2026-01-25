import { Navigate, createBrowserRouter } from "react-router-dom";
import type { ReactNode } from "react";
import LoginPage from "./pages/users/LoginPage.tsx";
import RegisterPage from "./pages/users/RegisterPage.tsx";
import Dashboard from "./pages/Dashboard";
import ProfilePage from "./pages/users/ProfilePage.tsx";
import TeamPage from "./pages/teams/TeamPage.tsx";
import CreateTeamPage from "./pages/teams/CreateTeamPage.tsx";
import MyTasksPage from "./pages/tasks/MyTasksPage.tsx";
import TaskPage from "./pages/tasks/TaskPage.tsx";
import CreatedTasksPage from "./pages/tasks/CreatedTasksPage.tsx";
import CreateTaskPage from "./pages/tasks/CreateTaskPage.tsx";
import AppLayout from "./components/AppLayout";
import { authStore } from "./auth/store";
import EditTaskPage from "./pages/tasks/EditTaskPage.tsx";
import EditProfilePage from "./pages/users/EditProfilePage.tsx";
import AverageEvaluationPage from "./pages/evaluations/AverageEvaluationPage.tsx";
import MyGivenEvaluationsPage from "./pages/evaluations/MyGivenEvaluationsPage.tsx";
import MyReceivedEvaluationsPage from "./pages/evaluations/MyReceivedEvaluationsPage.tsx";
import MyMeetingsPage from "./pages/meetings/MyMeetingsPage.tsx";
import CreateMeetingPage from "./pages/meetings/CreateMeetingPage.tsx";
import MeetingPage from "./pages/meetings/MeetingPage.tsx";
import CalendarPage from "./pages/calendar/CalendarPage.tsx";


const PrivateRoute = ({ children }: { children: ReactNode }) => {
  const { user } = authStore.getState();
  return user ? children : <Navigate to="/login" />;
};

const TasksRoute = ({
  children,
  allowedRoles,
}: {
  children: ReactNode;
  allowedRoles: string[];
}) => {
  const { user } = authStore.getState();
  if (!user) return <Navigate to="/login" />;
  if (!allowedRoles.includes(user.role)) return <Navigate to="/" />;
  return <>{children}</>;
};

export const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },
  {
    path: "/",
    element: (
      <PrivateRoute>
         <AppLayout>
           <Dashboard />
         </AppLayout>
      </PrivateRoute>
    ),
  },
  {
    path: "/profile",
    element: (
      <PrivateRoute>
        <AppLayout>
          <ProfilePage />
        </AppLayout>
      </PrivateRoute>
    ),
  },
  {
  path: "/profile/edit",
  element: (
    <PrivateRoute>
      <AppLayout>
        <EditProfilePage />
      </AppLayout>
    </PrivateRoute>
  ),
  },
  {
  path: "/team/:teamId",
  element: (
    <PrivateRoute>
      <AppLayout>
        <TeamPage />
      </AppLayout>
    </PrivateRoute>
    ),
  },
  {
  path: "/create-team",
  element: (
      <PrivateRoute>
          <AppLayout>
            <CreateTeamPage />
          </AppLayout>
      </PrivateRoute>
    ),
  },
    {
    path: "/tasks/my",
    element: (
      <TasksRoute allowedRoles={["employee", "manager"]}>
        <AppLayout>
          <MyTasksPage />
        </AppLayout>
      </TasksRoute>
    ),
  },
  {
    path: "/tasks/created",
    element: (
      <TasksRoute allowedRoles={["manager", "admin"]}>
        <AppLayout>
          <CreatedTasksPage />
        </AppLayout>
      </TasksRoute>
    ),
  },
  {
  path: "/tasks/create",
  element: (
    <PrivateRoute>
      <AppLayout>
        <CreateTaskPage />
      </AppLayout>
    </PrivateRoute>
  ),
  },
  {
  path: "/tasks/:taskId/edit",
  element: (
    <PrivateRoute>
      <AppLayout>
        <EditTaskPage />
      </AppLayout>
    </PrivateRoute>
  ),
  },
  {
    path: "/tasks/:taskId",
    element: (
      <PrivateRoute>
        <AppLayout>
          <TaskPage />
        </AppLayout>
      </PrivateRoute>
    ),
  },
    {
  path: "/evaluations/average",
  element: (
    <PrivateRoute>
      <AppLayout>
        <AverageEvaluationPage />
      </AppLayout>
    </PrivateRoute>
  ),
},
    {
  path: "/evaluations/my-given",
  element: (
    <TasksRoute allowedRoles={["admin", "manager"]}>
      <AppLayout>
        <MyGivenEvaluationsPage />
      </AppLayout>
    </TasksRoute>
  ),
},
    {
  path: "/evaluations/my-received",
  element: (
    <TasksRoute allowedRoles={["employee", "manager"]}>
      <AppLayout>
        <MyReceivedEvaluationsPage />
      </AppLayout>
    </TasksRoute>
  ),
},
    {
  path: "/meetings",
  element: (
    <PrivateRoute>
      <AppLayout>
        <MyMeetingsPage />
      </AppLayout>
    </PrivateRoute>
  ),
},
{
  path: "/meetings/create",
  element: (
    <TasksRoute allowedRoles={["manager", "admin"]}>
      <AppLayout>
        <CreateMeetingPage />
      </AppLayout>
    </TasksRoute>
  ),
},
{
  path: "/meetings/:id",
  element: (
    <PrivateRoute>
      <AppLayout>
        <MeetingPage />
      </AppLayout>
    </PrivateRoute>
  ),
},
    {
  path: "/calendar",
  element: (
    <PrivateRoute>
      <AppLayout>
        <CalendarPage />
      </AppLayout>
    </PrivateRoute>
  ),
},

]);
