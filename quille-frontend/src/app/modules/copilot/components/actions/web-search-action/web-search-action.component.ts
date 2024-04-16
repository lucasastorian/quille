import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Message } from '../../../../../services/message/message.service';

@Component({
  selector: 'web-search-action',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './web-search-action.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class WebSearchActionComponent {

  @Input() message: Message | undefined;

}
