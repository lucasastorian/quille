import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'prompt-suggestions',
  standalone: true,
  imports: [],
  templateUrl: './prompt-suggestions.component.html',
})
export class PromptSuggestionsComponent {

  @Output() onClick: EventEmitter<string> = new EventEmitter();

}
