import { Routes } from '@angular/router';
import { CopilotComponent } from './modules/copilot/copilot/copilot.component';

export const routes: Routes = [
    {
        path: "copilot",
        component: CopilotComponent
    },
    {
        path: "",
        redirectTo: "/copilot",
        pathMatch: "full"
    }
];

