import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Message } from '../../../../../services/message/message.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'inquire-action',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './inquire-action.component.html',
})
export class InquireActionComponent {

  @Input() message: Message | undefined;
  @Input() inProgress: boolean = false;
  @Input() terminal: boolean = false;
  @Output() onSubmit: EventEmitter<string> = new EventEmitter();

  public selectedOptions: { [key: string]: boolean } = {};
  public inputValue: string = '';
  public submitDisabled: boolean = true;
  public inputFocused: boolean = false;

  ngOnInit(): void {
    this._setForm();
  }

  private _setForm(): void {
    if (this.inProgress) {
      return;
    }

    if (this.message?.inquire) {
      if (this.message.inquire.input_value) {
        this.inputValue = this.message.inquire.input_value;
      }

      if (this.message.inquire.choices) {
        this.selectedOptions = Object.fromEntries(
          this.message.inquire.options.map(option => [option, this.message!.inquire!.choices.includes(option) || false])
        );
      }
    }
  }

  onSubmitClick() {
    const selectedOptions = Object.keys(this.selectedOptions).filter(option => this.selectedOptions[option]);
    const content = `${selectedOptions.join(', ')}\n ${this.inputValue}`.trim();
    this.onSubmit.emit(content);
  }

  get isSubmitEnabled() {
    const hasSelectedOptions = Object.values(this.selectedOptions).some(selected => selected);
    const hasInputValue = this.inputValue.trim() !== '';
    return hasSelectedOptions || hasInputValue;
  }

}
