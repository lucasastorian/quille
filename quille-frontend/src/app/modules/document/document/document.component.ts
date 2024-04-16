import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { NgxTiptapModule } from 'ngx-tiptap';
import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import Heading from '@tiptap/extension-heading';
import { mergeAttributes } from '@tiptap/core'
import { Highlight } from '@tiptap/extension-highlight';

@Component({
  selector: 'document',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    NgxTiptapModule
  ],
  templateUrl: './document.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DocumentComponent {

  @Input() form: FormGroup = new FormGroup({
    name: new FormControl(''),
    content: new FormControl('')
  })


  editor = new Editor({
    extensions: [
      StarterKit.configure({ heading: false }),
      Heading.configure({ levels: [1, 2, 3] }).extend({
        levels: [1, 2, 3],
        renderHTML({ node, HTMLAttributes }) {
          const level = this.options.levels.includes(node.attrs['level'])
            ? node.attrs['level']
            : this.options.levels[0]
          const classes: { [key: number]: string } = {
            1: 'text-4xl',
            2: 'text-3xl',
            3: 'text-2xl',
          }
          return [
            `h${level}`,
            mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, {
              class: `${classes[level]}`,
            }),
            0,
          ]
        },
      }),
      Placeholder.configure({
        placeholder: 'Type something...',
        emptyEditorClass: 'text-gray-700',
      }),
      Highlight.configure({
        HTMLAttributes: {
          class: 'bg-yellow-100',
        },
      })
    ],
    onUpdate: ({ editor }) => {
      if (editor.state.selection.empty) {
        return;
      }

      const selection = this.editor.view.state.selection;
      const from = selection.ranges[0].$from.pos;
      const to = selection.ranges[0].$to.pos;

      const range = this.editor.state.doc.textBetween(from, to, ' ');
      console.log(range);
    },
    editorProps: {
      attributes: {
        class: 'prose focus:outline-none max-w-none text-[18px] leading-normal bg-white min-h-screen [&_ol]:list-decimal [&_ul]:list-disc',
      },
    },
  });

}
