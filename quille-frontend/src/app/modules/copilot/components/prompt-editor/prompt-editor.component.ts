import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, ChangeDetectorRef, Component, ElementRef, EventEmitter, HostListener, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'prompt-editor',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './prompt-editor.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PromptEditorComponent implements OnChanges {

  // Used to focus the input field
  @ViewChild('textInput') promptInput: ElementRef<HTMLInputElement> | undefined;

  @Input() disabled: boolean = false;
  @Input() placeholder: string = 'Type something...'
  @Input() completionInProgress: boolean = false;
  @Output() onSubmit: EventEmitter<string> = new EventEmitter();

  promptControl = new FormControl('', [Validators.required]);

  constructor(private cdr: ChangeDetectorRef) {

  }

  // Update the prompt control when the disabled input changes
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['disabled']) {
      if (this.disabled) {
        this.promptControl.disable();
      } else {
        this.promptControl.enable();
      }
    }
  }

  // Focus the prompt input field
  public focus(): void {
    if (this.promptInput) {
      this.promptInput.nativeElement.focus();
    }
  }

  // Click enter to submit the prompt
  @HostListener("document:keydown", ["$event"]) onKeydownHandler(event: KeyboardEvent) {
    if (event.key === "Enter" && !this.disabled && this.promptControl.value !== "") {
      const prompt = this.promptControl.value!.trim();
      this.onSubmit.emit(prompt);
      this.promptControl.reset();
      this.cdr.detectChanges();
    }
  }

}
