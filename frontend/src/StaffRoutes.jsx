import { Route, Routes } from "react-router";
import { AdminArea, SignIn } from "./Admin.jsx";
import { EventWorkspace } from "./EventWorkspace.jsx";
import { ReviewDashboard } from "./ReviewDashboard.jsx";
import { ContentEditor } from "./ContentEditor.jsx";
import { ContentPreview } from "./ContentPreview.jsx";
import { Missing } from "./SiteLayout.jsx";

export default function StaffRoutes() {
  return (
    <Routes>
      <Route path="sign-in" element={<SignIn />} />
      <Route path="content/events/new" element={<EventWorkspace create />} />
      <Route path="content/events/:id" element={<EventWorkspace />} />
      <Route
        path="content/events/:id/preview"
        element={<EventWorkspace preview />}
      />
      <Route index element={<AdminArea key="dashboard" />} />
      <Route path="content/:kind/:id/preview" element={<ContentPreview />} />
      <Route path="settings/preview" element={<ContentPreview settings />} />
      <Route path="content/:kind/:id?" element={<ContentEditor />} />
      <Route path="media/:id?" element={<ContentEditor section="media" />} />
      <Route path="settings" element={<ContentEditor section="settings" />} />
      <Route path="recruitment" element={<ReviewDashboard />} />
      <Route
        path="recruitment/:cycleId/applications"
        element={<ReviewDashboard />}
      />
      <Route
        path="recruitment/:cycleId/applications/:applicationId"
        element={<ReviewDashboard />}
      />
      <Route
        path="content/events"
        element={<AdminArea key="events" events />}
      />
      <Route path="*" element={<Missing />} />
    </Routes>
  );
}
