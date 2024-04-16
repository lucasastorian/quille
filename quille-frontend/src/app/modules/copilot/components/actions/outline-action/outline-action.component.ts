import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { Message } from '../../../../../services/message/message.service';

@Component({
  selector: 'outline-action',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './outline-action.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OutlineActionComponent {

  @Input() message: Message | undefined;
  @Input() terminal: boolean = false;
  @Output() onSubmit: EventEmitter<string> = new EventEmitter<string>();

}
